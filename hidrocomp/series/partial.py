import pandas as pd
import math
import scipy.stats as stat
import plotly as py
import plotly.figure_factory as FF

from hidrocomp.statistic.genpareto import Gpa
from hidrocomp.graphics.gantt import Gantt
from hidrocomp.graphics.genpareto import GenPareto
from hidrocomp.graphics.hydrogram_parcial import HydrogramParcial
from hidrocomp.graphics.boxplot import Boxplot
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
        self.__peaks = None
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
        elif self.type_criterion == "duration_and_xmin":
            self.duration = kwargs['duration']


        self.__threshold(self.value)
        if self.type_criterion is not None:
            self.name = '%s(%s) - %s' % (self.dic_name[self.type_threshold], self.value, self.type_criterion.title())
        else:
            self.name = '%s(%s)' % (self.dic_name[self.type_threshold], self.value)

        if self.peaks is None:
            self.dist_gpa = Gpa(data=self.peaks["Peaks"])

    @property
    def peaks(self):
        if self.__peaks is None:
            self.__peaks = self.__criterion_water_resources_council()

        return self.__peaks

    def __events_over_threshold(self):

        data = self.data.loc[self.data[self.station] > self.threshold, self.station].to_frame()
        date_start, date_end = self.__start_and_end(data=data)
        _data = pd.DataFrame(index=pd.date_range(start=date_start, end=date_end))
        data = _data.combine_first(data[date_start:date_end])

        max_events = {'Date': list(), 'Peaks': list(), 'Start': list(), 'End': list(), "Duration": list()}
        events = self.__period_events(data=data, station=self.station)
        for i in events.index:
            start = events["Start"][i]
            end = events["Finish"][i]
            duration = (end - start)
            peaks = data[start:end].max()[0]
            date_max = data[start:end].idxmax()[0]
            max_events["Date"].append(date_max)
            max_events["Peaks"].append(peaks)
            max_events["Start"].append(start)
            end = end + pd.timedelta_range(start='1 day', periods=1, freq='D')
            max_events["End"].append(end.values[0])
            max_events["Duration"].append(duration.days + 1)

        df = pd.DataFrame(data=max_events, index=max_events["Date"], columns=['Peaks', 'Start', 'End', 'Duration'])
        return df

    def __duration(self):
        events_over_threshold = self.__events_over_threshold().sort_values(by="Peaks", ascending=False)

        events_duration = pd.DataFrame()

        for i in events_over_threshold.index:
            actual = events_over_threshold.loc[events_over_threshold.index == i]

            if len(events_duration) == 0:
                events_duration = events_duration.combine_first(actual)
                events_duration.at[i, "Date"] = i

            else:
                if_add = False
                for j in events_duration.index:
                    duration = i - j
                    if abs(duration.days) <= self.duration:
                        events_duration = self.__update_peaks(actual=actual, events=events_duration, idx=j)
                        if_add = True
                        break
                if not if_add:
                    events_duration = events_duration.combine_first(actual)
                    events_duration.at[i, "Date"] = i

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

    @staticmethod
    def __update_peaks(actual, events, idx):
        if actual.index.values[0] > idx:
            end = actual["End"].values[0]
            start = events["Start"][idx]
        else:
            end = events["End"][idx]
            start = actual["Start"].values[0]
        events["Start"][idx] = start
        events["End"][idx] = end

        duration_into_events = end - start
        events["Duration"][idx] = duration_into_events.days

        peaks = [actual["Peaks"].values[0], events["Peaks"][idx]]
        date_peaks = [actual.index.values[0], events["Date"][idx]]
        peak_idx_max = peaks.index(max(peaks))
        date = date_peaks[peak_idx_max]
        peaks = peaks[peak_idx_max]
        events["Peaks"][idx] = peaks
        events.at[idx, "Date"] = date

        return events

    def __criterion_water_resources_council(self):
        """
        Events dependents
        theta < 5days + log(A) or (3/4)*min[Q1, Q2]
        """
        events_duration = self.__duration()

        events_wrc = pd.DataFrame()

        for i in events_duration.index:
            actual = events_duration.loc[events_duration.index == i]

            if len(events_wrc) == 0:
                events_wrc = events_wrc.combine_first(actual)
                events_wrc.at[i, "Date"] = i

            else:
                date_range = pd.date_range(events_wrc.iloc[-1].name, i)
                qmin = self.data[self.station].loc[date_range].min()
                q1 = events_duration.iloc[-1].Peaks
                q2 = actual["Peaks"][i]

                if qmin < (3/4)*min([q1, q2]):
                    events_wrc = events_wrc.combine_first(actual)
                    events_wrc.at[i, "Date"] = i
                else:
                    events_wrc = self.__update_peaks(actual=actual, events=events_wrc)

        events_wrc = events_wrc.set_index("Date")
        return events_wrc

    @staticmethod
    def __start_and_end(data):
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

    def plot_distribution(self, title, type_function, save=False):
        parameter = self.dist_gpa.parameter
        genpareto = GenPareto(title, shape=parameter["shape"], location=parameter["loc"], scale=parameter["scale"])
        data, fig = genpareto.plot(type_function)
        if save:
            aux_name = title.replace(' ', '_')
            py.image.save_as(fig, filename='gráficos/' + '%s.png' % aux_name)
        return data, fig

    def plot_boxplot_resample(self, magn_resample, name, save=False):

        data, fig = Boxplot(magn_resample=magn_resample, name=name).plot()
        if save:
            py.image.save_as(fig, filename='gráficos/boxplot_%s.png' % name)

        return fig, data

    def plot_spells(self, title, size_text=14):
        df_spells, df, month_start, month_end = Gantt.get_spells(data_peaks=self.peaks,
                                                                 month_water=[self.obj.month_num, self.obj.month_abr])

        df_spells = df_spells.sort_values('Task', ascending=False).reset_index(drop=True)

        colors = '#000000'
        fig = FF.create_gantt(df_spells, group_tasks=True, colors=colors, title=title, height=900, width=1200)

        fig['layout'].update(autosize=True)
        fig['layout']['xaxis'].update(title="Mês", range=[month_start, month_end], tickformat="%b")
        fig['layout']['yaxis'].update(title="Ano")
        fig['layout']['xaxis']['rangeselector'] = {}
        fig.layout.title = dict(text=title, x=0.5, xanchor='center', y=0.9, yanchor='top',
                                font=dict(family='Courier New, monospace', color='#7f7f7f', size=size_text + 6))
        fig.layout.font = dict(family='Courier New, monospace', size=size_text, color='#7f7f7f')
        fig.layout.plot_bgcolor = 'rgba(0,0,0,0)'
        return fig, df_spells

    def polar(self,  width=900, height=900, size_text=14, title=None, color=None, name=None):
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

        _polar = Polar(df_events=self.peaks)
        fig, data = _polar.plot(width=width, height=height, size_text=size_text, title=title, color=color, name=name)

        return fig, data

    def hydrogram(self, title, width=None, height=None, size_text=16, color=None):
        hydrogram = HydrogramParcial(data=self.data, peaks=self.peaks, threshold=self.threshold, station=self.station,
                                     threshold_criterion=None, title=title, width=width,
                                     type_criterion=None, height=height, size_text=size_text,
                                     color=color)
        fig, data = hydrogram.plot()
        return fig, data
