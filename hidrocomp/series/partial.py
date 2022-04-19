import pandas as pd
import math
import plotly as py
import plotly.figure_factory as FF

from hidrocomp.statistic.genpareto import Gpa
from hidrocomp.graphics.gantt import Gantt
from hidrocomp.graphics.genpareto import GenPareto
from hidrocomp.graphics.hydrogram_parcial import HydrogramParcial
from hidrocomp.graphics.polar import Polar


class Partial(object):
    distribution = 'GPA'
    __percentil = 0.8
    dic_name = {'stationary': 'Percentil', 'events_by_year': 'Eventos por Ano', 'autocorrelation': 'Autocorrelação'}

    def __init__(self, obj, station, type_threshold, value_threshold, type_event, type_criterion, **kwargs):
        """
            Parameter:
                obj: Object Series;
                station: Point observation of date
                type_threshold: Tipo de calculo do limiar('stationary' or
                                                          'events_by_year')
                value_threshold: Valor do limiar:
                    Para type_threshold = 'stationary': percentil ou valor
                    Para type_threshold = 'events_by_year': quantidade média de
                                                            picos por ano
                type_criterion: Critério de Independência ('mean', 'median',
                                'xmin_bigger_dois_terco_x', 'xmin_bigger_qmin')
                type_event: Tipo do evento em estudo ('flood' or 'drought')
        """
        self.obj = obj
        self.data = self.obj.data
        self.station = station
        self.__information = None
        self.threshold_criterion = None
        self.fit = None
        self.type_threshold = type_threshold
        self.type_criterion = type_criterion
        self.type_event = type_event
        self.value = value_threshold

        if self.type_criterion == 'median':
            self.__percentil = 0.65
        elif self.type_criterion == 'autocorrelation':
            self.duration = kwargs['duration']
        elif self.type_criterion == "wrc":
            self.duration = kwargs['duration']
        elif self.type_criterion == 'duration':
            self.duration = kwargs['duration']

        self.__threshold(self.value)
        if self.type_criterion is not None:
            self.name = '%s(%s) - %s' % (self.dic_name[self.type_threshold], self.value, self.type_criterion.title())
        else:
            self.name = '%s(%s)' % (self.dic_name[self.type_threshold], self.value)

        if self.__information is not None:
            self.dist_gpa = Gpa(data=self.information["Peaks"])

    def __str__(self) -> str:
        return self.__information.__str__()

    def __repr__(self) -> str:
        return self.__information.__repr__()

    @property
    def events(self) -> pd.DataFrame:
        """
        Peaks - Flow Peaks the events.
        NDBE - Number of Days Before the Events.
        Duration - Duration the Events.
        PEY - Position of the Event in the Year.
        NDTP - Number of Days to Peak from the start of the event.
        Type - Type the events in the year, e.g (1, 2, ... n)
        """
        events = pd.DataFrame(columns=['Peaks', 'NDBE', 'Duration', 'PEY', 'NDTP', 'Date peak'])
        events['Peaks'] = self.information['Peaks']
        events['NDBE'] = self.number_days_before_events
        events['Duration'] = self.__information['Duration']
        events['PEY'] = self.julian()
        events['NDTP'] = self.number_days_to_peaks
        events = events.combine_first(self.type_events_year)
        events['Date peak'] = events.index
        events.set_index(['Year', 'Type'], inplace=True)
        return events[['Peaks', 'NDBE', 'Duration', 'PEY', 'NDTP', 'Date peak']]

    @property
    def peaks(self):
        if self.__information is None:
            return self.information['Peaks']
        return self.__information['Peaks']

    @property
    def information(self) -> pd.Series:
        if self.__information is None:
            if self.type_criterion == "wrc":
                if self.type_event == "flood":
                    self.__information = self.__criterion_water_resources_council()
                elif self.type_event == "drought":
                    self.__information = self.__events_over_threshold()
                    if len(self.__information) > 0:
                        self.__information.at[self.__information.sort_values(by="End").index[-1],
                                        "End"] = self.__information.sort_values(
                            by="End")["End"].iloc[-1] - pd.to_timedelta(1, unit="d")

            elif self.type_criterion == "duration":
                if self.type_event == "flood":
                    self.__information = self.__duration()
                elif self.type_event == "drought":
                    self.__information = self.__duration()
                    if len(self.__information) > 0:
                        self.__information.at[self.__information.sort_values(by="End").index[-1],
                                        "End"] = self.__information.sort_values(
                            by="End")["End"].iloc[-1] - pd.to_timedelta(1, unit="d")

            elif self.type_criterion == "autocorrelation":
                if self.type_event == "flood":
                    self.__information = self.__test_autocorrelation()
                elif self.type_event == "drought":
                    self.__information = self.__test_autocorrelation()
                    if len(self.__information) > 0:
                        self.__information.at[self.__information.sort_values(by="End").index[-1],
                                        "End"] = self.__information.sort_values(
                            by="End")["End"].iloc[-1] - pd.to_timedelta(1, unit="d")
            else:
                if self.type_event == "flood":
                    self.__information = self.__events_over_threshold()
                elif self.type_event == "drought":
                    self.__information = self.__events_over_threshold()
                    if len(self.__information) > 0:
                        self.__information.at[self.__information.sort_values(by="End").index[-1],
                                        "End"] = self.__information.sort_values(
                            by="End")["End"].iloc[-1] - pd.to_timedelta(1, unit="d")

        self.__information = self.__information.sort_index()
        return self.__information

    def __events_over_threshold(self):

        if self.type_event == 'flood':
            data = self.data.loc[self.data[self.station] > self.threshold, self.station].to_frame()

        elif self.type_event == 'drought':
            data = self.data.loc[self.data[self.station] < self.threshold, self.station].to_frame()

        else:
            raise TypeError("Type events {} invalid! Use flood or drought".format(self.type_event))

        date_start, date_end = self.__start_and_end(data=data)
        if date_start is not None and date_end is not None:
            _data = pd.DataFrame(index=pd.date_range(start=date_start, end=date_end))
            data = _data.combine_first(data[date_start:date_end])

        max_events = {'Date': list(), 'Peaks': list(), 'Start': list(), 'End': list(),
                      'Duration': list(), 'Julian': list()
                      }
        events = self.__period_events(data=data, station=self.station)
        for i in events.index:
            start = events["Start"][i]
            end = events["Finish"][i]
            duration = (end - start)
            if self.type_event == "flood":
                peaks = data[start:end].max()[0]
                date_peak = data[start:end].idxmax()[0]
            else:
                peaks = data[start:end].min()[0]
                date_peak = data[start:end].idxmin()[0]

            max_events["Date"].append(date_peak)
            max_events['Julian'].append(int(date_peak.strftime("%j")))
            max_events["Peaks"].append(peaks)
            max_events["Start"].append(start)
            end = end + pd.timedelta_range(start='1 day', periods=1, freq='D')
            max_events["End"].append(end.values[0])
            max_events["Duration"].append(duration.days + 1)

        df = pd.DataFrame(data=max_events, index=max_events["Date"],
                          columns=['Peaks', 'Start', 'End', 'Duration', 'Julian']).sort_values(by='End')
        return df

    def __duration(self):
        events_over_threshold = self.__events_over_threshold().sort_values(by="Peaks", ascending=False)

        events_duration = pd.DataFrame()

        for i in events_over_threshold.index:
            actual = events_over_threshold.loc[events_over_threshold.index == i]

            if len(events_duration) == 0:
                if self.type_event == 'flood':
                    events_duration = events_duration.combine_first(actual).sort_values(by="Peaks", ascending=False)
                elif self.type_event == 'drought':
                    events_duration = events_duration.combine_first(actual).sort_values(by="Peaks", ascending=True)
                else:
                    raise TypeError("Type events {} invalid! Use flood or drought".format(self.type_event))

                events_duration.at[i, "Date"] = i
            else:
                if_add = False
                for j in events_duration.index:
                    duration = i - j
                    if abs(duration.days) <= self.duration:
                        if self.type_event == 'flood':
                            events_duration = self.__update_peaks(actual=actual, events=events_duration,
                                                                  idx=j).sort_values(by="Peaks", ascending=False)
                        elif self.type_event == 'drought':
                            events_duration = self.__update_peaks(actual=actual, events=events_duration,
                                                                  idx=j).sort_values(by="Peaks", ascending=True)
                        else:
                            raise TypeError("Type events {} invalid! Use flood or drought".format(self.type_event))

                        if_add = True
                        break
                if not if_add:
                    if self.type_event == 'flood':
                        events_duration = events_duration.combine_first(actual).sort_values(by="Peaks", ascending=False)
                    elif self.type_event == 'drought':
                        events_duration = events_duration.combine_first(actual).sort_values(by="Peaks", ascending=True)
                    else:
                        raise TypeError("Type events {} invalid! Use flood or drought".format(self.type_event))

                    events_duration.at[i, "Date"] = i

        if len(events_duration) > 0:
            events_duration = events_duration.set_index("Date")

        return events_duration

    def __threshold(self, value):
        if value > 1 and self.type_threshold == 'events_by_year':
            self.threshold = self.data[self.station].quantile(self.__percentil)
        elif value > 1 and self.type_threshold == 'stationary':
            self.threshold = value
        else:
            self.threshold = self.data[self.station].quantile(value)
        return self.threshold

    def __test_autocorrelation(self):
        peaks = self.__duration()
        try:
            n = len(peaks.Peaks)
            serie = pd.Series(peaks.Peaks, index=peaks.index)
            self.lag1 = serie.autocorr(lag=1)
            self.lag2 = serie.autocorr(lag=2)
            r11_n = (-1 + 1.645 * math.sqrt(n - 1 - 1)) / (n - 1)
            r12_n = (-1 - 1.645 * math.sqrt(n - 1 - 1)) / (n - 1)
            r21_n = (-1 + 1.645 * math.sqrt(n - 2 - 1)) / (n - 2)
            r22_n = (-1 - 1.645 * math.sqrt(n - 2 - 1)) / (n - 2)

            if r11_n > self.lag1 > r12_n and r21_n > self.lag2 > r22_n:
                self.duration += 1
                return self.__test_autocorrelation()
            return peaks
        except (AttributeError, ValueError):
            return peaks

    def __update_peaks(self, actual, events, idx):
        if actual["End"].values[0] > events["End"][idx]:
            end = actual["End"].values[0]
        else:
            end = events["End"][idx]

        if actual["Start"].values[0] > events["Start"][idx]:
            start = events["Start"][idx]
        else:
            start = actual["Start"].values[0]

        events["Start"][idx] = start
        events["End"][idx] = end

        duration_into_events = end - start
        events["Duration"][idx] = duration_into_events.days

        peaks = [actual["Peaks"].values[0], events["Peaks"][idx]]
        date_peaks = [actual.index.values[0], events["Date"][idx]]
        if self.type_event == 'flood':
            peak_idx_max = peaks.index(max(peaks))
        elif self.type_event == 'drought':
            peak_idx_max = peaks.index(min(peaks))
        else:
            raise TypeError("Type events {} invalid! Use flood or drought".format(self.type_event))

        date = date_peaks[peak_idx_max]
        peaks = peaks[peak_idx_max]
        events["Peaks"][idx] = peaks
        events.at[idx, "Date"] = date

        return events

    @property
    def events_by_year(self):
        n_year = self.obj.end_date.year - self.obj.start_date.year
        n_events = len(self.information)

        return n_events/n_year

    def __criterion_water_resources_council(self):
        """
        Events dependents
        theta < 5days + log(A) or (3/4)*min[Q1, Q2]
        """
        try:
            events_duration = self.__duration().sort_values(by="Peaks", ascending=False)

            events_wrc = pd.DataFrame()
            for i in events_duration.index:
                actual = events_duration.loc[events_duration.index == i]

                if len(events_wrc) == 0:
                    events_wrc = events_wrc.combine_first(actual).sort_values(by="Peaks", ascending=False)
                    events_wrc.at[i, "Date"] = i

                else:
                    if_add = False
                    for j in events_wrc.index:
                        date_range = pd.date_range(j, i)
                        qmin = self.data[self.station].loc[date_range].min()
                        q1 = events_wrc["Peaks"][j]
                        q2 = actual["Peaks"][i]

                        if qmin > (3/4)*min([q1, q2]):
                            events_wrc = self.__update_peaks(actual=actual, events=events_wrc,
                                                             idx=j).sort_values(by="Peaks", ascending=False)
                            if_add = True
                            break
                    if not if_add:
                        events_wrc = events_wrc.combine_first(actual).sort_values(by="Peaks", ascending=False)
                        events_wrc.at[i, "Date"] = i

            if len(events_wrc) > 0:
                events_wrc = events_wrc.set_index("Date")
        except KeyError:
            events_wrc = self.__duration()
        return events_wrc

    @staticmethod
    def __start_and_end(data):
        if len(data) == 0:
            return None, None
        try:
            boolean = data.dropna(axis=0, how='all')
        except AttributeError:
            boolean = data
        date = boolean.index
        return date[0], date[-1]

    @staticmethod
    def __period_events(data, station):
        """
        """
        aux = list()
        list_start = list()
        list_end = list()
        gantt_bool = data[station].isnull()
        for i in gantt_bool.index:
            if ~gantt_bool.loc[i]:
                aux.append(i)
            elif len(aux) >= 1 and gantt_bool.loc[i]:
                list_start.append(aux[0])
                list_end.append(aux[-1])
                aux = []
        if len(aux) > 0:
            list_start.append(aux[0])
            list_end.append(aux[-1])

        dic = {'Start': list_start, 'Finish': list_end}
        return pd.DataFrame(dic)

    def magnitude(self, period_return, estimador):
        if estimador == 'MML':
            self.dist_gpa.mml()
        elif estimador == 'MVS':
            self.dist_gpa.mvs()

        p = 1 - (1 / period_return)
        return self.dist_gpa.values(p)

    def period_return(self, magnitude, estimador):
        if estimador == 'MML':
            self.dist_gpa.mml()
        elif estimador == 'MVS':
            self.dist_gpa.mvs()

        p = self.dist_gpa.probs(magnitude)
        return 1 / (1 - p)

    def number_start_month_year_hydrological(self) -> int:
        if self.type_event == 'flood':
            return self.obj.month_num_flood

        elif self.type_event == 'drought':
            return self.obj.month_num_drought

        else:
            raise TypeError("Type events {} invalid! Use flood or drought".format(self.type_event))

    def abbr_start_month_year_hydrological(self) -> str:
        if self.type_event == 'flood':
            return self.obj.month_abr_flood

        elif self.type_event == 'drought':
            return self.obj.month_abr_drought

        else:
            raise TypeError("Type events {} invalid! Use flood or drought".format(self.type_event))

    def julian_radius(self, type_year='hydrological', start_events=False):
        if type_year == 'hydrological':
            month = self.number_start_month_year_hydrological()
        else:
            month = 1

        if start_events:
            julian_day = self.__obtain_julian(month=month, dates_events=self.information.Start, radius=True)
        else:
            julian_day = self.__obtain_julian(month=month, dates_events=self.information.index, radius=True)

        return julian_day

    def julian(self, type_year='hydrological', start_events=False):
        if type_year == 'hydrological':
            month = self.number_start_month_year_hydrological()
        else:
            month = 1

        if start_events:
            julian_day = self.__obtain_julian(month=month, dates_events=self.information.Start, radius=False)
        else:
            julian_day = self.__obtain_julian(month=month, dates_events=self.information.index, radius=False)

        return julian_day

    def occurrence_dates_graus(self, start_day: int, start_month: int, end_day: int, end_month: int) -> pd.Series:
        dates = self.information.index
        # start_date = pd.to_datetime(start_, dayfirst=True)
        # end_date = pd.to_datetime(end_date, dayfirst=True)

        df_occurrence_dates = pd.Series(name='Date')

        for date in dates:
            date_range = pd.date_range(
                start=pd.to_datetime(f'{start_day}-{start_month}-{date.year}', dayfirst=True),
                end=pd.to_datetime(f'{end_day}-{end_month}-{date.year}', dayfirst=True),
                freq='D'
            )
            length = date_range.size
            try:
                idx = date_range.get_loc(date)
                df_occurrence_dates.at[date] = (idx+1) / length * 360
            except KeyError:
                pass

        return df_occurrence_dates

    @property
    def number_days_before_events(self) -> pd.Series:

        if self.__information is None:
            return self.events['NDBE']

        series = pd.Series(name='NDBE')
        for date, information in self.__information.groupby(pd.Grouper(freq=self.abbr_start_month_year_hydrological())):
            count = 0
            index_o = None
            for index in information.index:
                if count == 0:
                    series.at[index] = int((information['Start'][index] - date).days)
                    index_o = index
                else:
                    series.at[index] = int((information['Start'][index] - information['End'][index_o]).days)
                    index_o = index

                count += 1

        return series

    @property
    def type_events_year(self) -> pd.DataFrame:
        df = pd.DataFrame(columns=['Type', 'Year'])
        for date, information in self.__information.groupby(pd.Grouper(freq=self.abbr_start_month_year_hydrological())):
            count = 1
            for idx in information.index:
                df.at[idx, 'Type'] = count
                df.at[idx, 'Year'] = date.year
                count += 1
        return df

    @property
    def number_days_to_peaks(self) -> pd.Series:

        series = pd.Series(name='NDTP')
        for index in self.__information.index:
            series.at[index] = int((index - self.__information['Start'][index]).days)

        return series

    @staticmethod
    def __obtain_julian(month: int, dates_events, radius=False) -> pd.Series:
        df_julian = pd.Series(name='Julian')
        for date in dates_events:
            day_julian = int(date.strftime("%j"))
            nd = len(pd.date_range(start=pd.to_datetime(f'01-01-{date.year}', dayfirst=True),
                                   end=pd.to_datetime(f'31-12-{date.year}', dayfirst=True),
                                   freq='D'))

            start_day = int(pd.to_datetime(f'01-{month}-{date.year}', dayfirst=True).strftime("%j"))

            if day_julian >= start_day:
                day = (day_julian - start_day)
            else:
                day = ((nd - start_day) + day_julian)

            if radius:
                transformation_day = day * (360 / nd)
                if transformation_day > 360:
                    df_julian.at[date] = transformation_day - 360
                else:
                    df_julian.at[date] = transformation_day
            else:
                df_julian.at[date] = (nd - start_day) + day_julian

        return df_julian

    # TODO Rename of spells
    def plot_distribution(self, title, function_type, save=False):
        parameter = self.dist_gpa.parameter
        genpareto = GenPareto(title, shape=parameter["shape"], location=parameter["loc"], scale=parameter["scale"])
        data, fig = genpareto.plot(function_type)
        if save:
            aux_name = title.replace(' ', '_')
            py.image.save_as(fig, filename='gráficos/' + '%s.png' % aux_name)
        return data, fig

    # TODO Rename of spells
    def plot_spells(self, title, size_text=14):
        if self.type_event == "drought":
            month_start_abr, month_start_num = self.obj.month_abr_drought, self.obj.month_num_drought
        elif self.type_event == "flood":
            month_start_abr, month_start_num = self.obj.month_abr_flood, self.obj.month_num_flood
        else:
            raise TypeError

        df_spells, df, month_start, month_end = Gantt.get_spells(data_peaks=self.information,
                                                                 month_water=[month_start_num, month_start_abr])

        df_spells = df_spells.sort_values('Task', ascending=False).reset_index(drop=True)

        colors = '#000000'
        fig = FF.create_gantt(df_spells, group_tasks=True, colors=colors, title=title, height=900, width=1200)

        fig['layout'].update(autosize=True)
        fig['layout']['xaxis'].update(title="Month", range=[month_start, month_end], tickformat="%b")
        fig['layout']['yaxis'].update(title="Year")
        fig['layout']['xaxis']['rangeselector'] = {}
        fig.layout.title = dict(text=title, x=0.5, xanchor='center', y=0.9, yanchor='top',
                                font=dict(family='Courier New, monospace', color='#7f7f7f', size=size_text + 6))
        fig.layout.font = dict(family='Courier New, monospace', size=size_text, color='#7f7f7f')
        fig.layout.plot_bgcolor = 'rgba(0,0,0,0)'
        return fig, df_spells

    # TODO Rename of polar
    # TODO Add parameters language and showlegend
    def plot_polar(self, title: str = None, width: int = 900, height: int = 900, size_text: int = 14,
                   color=None, name=None, with_duration: bool = False, showlegend: bool = False, language: str = 'pt'):
        if self.type_event == 'flood':
            if title is None:
                title = 'Maximum Partial'
            elif name is None:
                name = 'Maximum peaks'
        elif self.type_event == 'drought':
            if title is None:
                title = 'Minimum Partial'
            elif name is None:
                name = 'Minimum peaks'

        _polar = Polar(df_events=self.information)
        fig, data = _polar.plot(width=width, height=height, size_text=size_text, title=title, color=color, name=name,
                                with_duration=with_duration, showlegend=showlegend, language=language)

        return fig, data

    # TODO Rename of hydrogram
    # TODO Add parameters language and showlegend
    def plot_hydrogram(self, title, width=None, height=None, size_text=16, color=None, threshold_line: bool = True,
                       point_start_end: bool = True):
        hydrogram = HydrogramParcial(data=self.data, peaks=self.information, threshold=self.threshold,
                                     station=self.station, threshold_criterion=self.threshold_criterion, title=title,
                                     width=width, type_criterion=self.type_criterion, height=height,
                                     size_text=size_text, color=color, line_threshold=threshold_line,
                                     point_start_end=point_start_end)
        fig, data = hydrogram.plot()
        return fig, data
