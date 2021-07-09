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


class Parcial(object):
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
        self.peaks = None
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
            self.event_peaks()
            self.dist_gpa = Gpa(data=self.peaks["peaks"])

    def test_peaks(self):

        events_threshold = self.__events_over_threshold(self.threshold)[0]
        print(events_threshold)

    def event_peaks(self):
        max_events = {'Date': list(), 'peaks': list(), 'Start': list(), 'End': list(),
                      'Duration': list()}

        events_criterion, self.threshold_criterion = self.__events_over_threshold()
        events_threshold = self.__events_over_threshold(self.threshold)[0]

        idx_before = events_threshold.index[0]
        low_limiar = False

        data = {'Date': list(), 'peaks': list()}
        data_min = {'Date': list(), 'peaks': list()}
        start = False
        for i in events_threshold.index:
            if not start:
                if events_threshold.loc[i]:
                    start = False
                else:
                    start = True
            if events_threshold.loc[i] and start:
                data['peaks'].append(self.data.loc[i, self.station])
                data['Date'].append(i)
                low_limiar = True
                data_min['peaks'].append(self.data.loc[i, self.station])
                data_min['Date'].append(i)
            else:
                if low_limiar:
                    data['peaks'].append(self.data.loc[idx_before, self.station])
                    data['Date'].append(i)
                    data['peaks'].append(self.data.loc[i, self.station])
                    data['Date'].append(i)
                    low_limiar = False
                    data_min['peaks'].append(self.data.loc[i, self.station])
                    data_min['Date'].append(i)
                # else:
                data, max_events, data_min = self.__criterion(data=data, max_events=max_events, data_min=data_min,
                                                              events_criterion=events_criterion.loc[i])
            idx_before = i

        self.peaks = pd.DataFrame(
            max_events, columns=['Duration', 'Start', 'End', 'peaks'],
            index=max_events['Date']
        )

        if (self.type_criterion == 'autocorrelation'
                and self.test_autocorrelation()[0]):
            self.duration += 1
            return self.event_peaks()
        if (self.type_threshold == 'events_by_year'
                and self.__test_threshold_events_by_year(self.peaks, self.value)):
            return self.event_peaks()
        return self.peaks

    def __peaks_type_event(self, lista):
        if self.type_event == "flood":
            return max(lista)
        elif self.type_event == "drought":
            return min(lista)
        else:
            return "Type Event Erro!"

    def __events_over_threshold(self, threshold=None):
        if threshold is None:
            if self.type_criterion == 'mean':
                threshold = self.data[self.station].mean()
            elif self.type_criterion == 'median':
                threshold = self.data[self.station].median()
            elif self.type_criterion is None:
                threshold = self.threshold

        if self.type_event == 'flood':
            events = self.data[self.station].isin(self.data.loc[self.data[
                                                                    self.station] > threshold, self.station])
            return events, threshold

        elif self.type_event == 'drought':
            events = self.data[self.station].isin(self.data.loc[self.data[
                                                                    self.station] < threshold, self.station])
            return events, threshold

        else:
            return 'Event error!'

    def __threshold(self, value):
        if value > 1 and self.type_threshold == 'events_by_year':
            self.threshold = self.data[self.station].quantile(self.__percentil)
        elif value > 1 and self.type_threshold == 'stationary':
            self.threshold = value
        else:
            self.threshold = self.data[self.station].quantile(value)
        return self.threshold

    def __test_threshold_events_by_year(self, peaks=None, value=None):
        n_year = self.obj.date_end.year - self.obj.date_start.year

        if len(peaks) + 1 < int(value * n_year):
            self.__percentil -= 0.005
            self.__threshold(self.__percentil)
            return True
        elif len(peaks) > (int(value * n_year) + 2):
            self.__percentil += 0.005
            self.__threshold(self.__percentil)
            return True
        return False

    def __criterion(self, **kwargs):
        if self.type_criterion == 'mean':
            data, max_events = self.__criterion_mean(data=kwargs['data'], max_events=kwargs['max_events'],
                                                     events_criterion=kwargs['events_criterion'])
            return data, max_events, kwargs['data_min']

        elif self.type_criterion == 'median':
            data, max_events = self.__criterion_median(data=kwargs['data'], max_events=kwargs['max_events'],
                                                       events_criterion=kwargs['events_criterion'])
            return data, max_events, kwargs['data_min']

        elif self.type_criterion == 'autocorrelation':
            data, max_events = self.__criterion_duration(data=kwargs['data'], max_events=kwargs['max_events'],
                                                         events_criterion=kwargs['events_criterion'])
            return data, max_events, kwargs['data_min']

        elif self.type_criterion == 'xmin_bigger_qmin':
            return self.__criterion_xmin_bigger_qmin(max_events=kwargs['max_events'], data_min=kwargs['data_min'],
                                                     data=kwargs['data'], events_criterion=kwargs['events_criterion'])

        elif self.type_criterion == 'xmin_bigger_dois_terco_x':
            return self.__criterion_xmin_bigger_dois_terco_x(data=kwargs['data'], max_events=kwargs['max_events'],
                                                             data_min=kwargs['data_min'],
                                                             events_criterion=kwargs['events_criterion'])

        elif self.type_criterion == 'duration_and_xmin':
            # self.duration = 5 + math.log(self.obj.inf_stations[self.station].area, 2)
            return self.__criterion_duration_and_xmin(data=kwargs['data'], max_events=kwargs['max_events'],
                                                      data_min=kwargs['data_min'],
                                                      events_criterion=kwargs['events_criterion'])

        elif self.type_criterion == 'duration':
            data, max_events = self.__criterion_duration(data=kwargs['data'], max_events=kwargs['max_events'],
                                                         events_criterion=kwargs['events_criterion'])
            return data, max_events, kwargs['data_min']

        elif self.type_criterion is None:
            data, max_events = self.__criterion_none(data=kwargs['data'], max_events=kwargs['max_events'])
            return data, max_events, kwargs['data_min']

    def __criterion_mean(self, data, max_events, events_criterion):
        if len(data['peaks']) > 0 and (not events_criterion):
            return self.__add_peaks(data, max_events)
        else:
            return data, max_events

    def __criterion_median(self, data, max_events, events_criterion):
        if len(data['peaks']) > 0 and (not events_criterion):
            return self.__add_peaks(data, max_events)
        else:
            return data, max_events

    def __criterion_none(self, data, max_events):
        if len(data['peaks']) > 0:
            return self.__add_peaks(data, max_events)
        else:
            return data, max_events

    def __criterion_duration(self, data, max_events, events_criterion):
        if not events_criterion:
            if len(data['peaks']) == 0:
                return data, max_events
            elif len(max_events['Date']) == 0:
                return self.__add_peaks(data, max_events)
            else:
                if self.__test_duration(data, max_events):
                    data, max_events = self.__troca_peaks(data, max_events)
                    return data, max_events
                return self.__add_peaks(data, max_events)
        else:
            return data, max_events

    def __criterion_xmin_bigger_qmin(self, data, max_events, data_min, events_criterion):
        if not events_criterion:
            if len(data['Date']) == 0:
                return data, max_events, data_min
            elif len(max_events['Date']) == 0:
                data, max_events = self.__add_peaks(data, max_events)
                data_min = {'Date': [], 'peaks': []}
                return data, max_events, data_min
            elif len(data_min) == 0:
                return data, max_events, data_min
            else:
                if self.__test_xmin_bigger_q(data, max_events, data_min):
                    data, max_events = self.__troca_peaks(data, max_events)
                    data_min = {'Date': [], 'peaks': []}
                    return data, max_events, data_min
                data, max_events = self.__add_peaks(data, max_events)
                data_min = {'Date': [], 'peaks': []}
                return data, max_events, data_min
        else:
            return data, max_events, data_min

    def __criterion_xmin_bigger_dois_terco_x(self, data, max_events, data_min, events_criterion):
        if not events_criterion:
            if len(data['Date']) == 0:
                return data, max_events, data_min
            elif len(max_events['Date']) == 0:
                data, max_events = self.__add_peaks(data, max_events)
                data_min = {'Date': [], 'peaks': []}
                return data, max_events, data_min
            elif len(data_min) == 0:
                return data, max_events, data_min
            else:
                if self.__test_xmin_bigger_dois_terco_x(data, max_events, data_min) and self.__test_duration(data, max_events):
                    data, max_events = self.__troca_peaks(data, max_events)
                    data_min = {'Date': [], 'peaks': []}
                    return data, max_events, data_min
                data, max_events = self.__add_peaks(data, max_events)
                data_min = {'Date': [], 'peaks': []}
                return data, max_events, data_min
        else:
            return data, max_events, data_min

    def __criterion_duration_and_xmin(self, data, max_events, events_criterion, data_min):
        if not events_criterion:
            if len(data['Date']) == 0:
                return data, max_events, data_min
            elif len(max_events['Date']) == 0:
                data, max_events = self.__add_peaks(data, max_events)
                data_min = {'Date': [], 'peaks': []}
                return data, max_events, data_min
            elif len(data_min) == 0:
                return data, max_events, data_min
            else:
                if self.__test_xmin_bigger_q(data, max_events, data_min) or self.__test_duration(data, max_events):
                    data, max_events = self.__troca_peaks(data, max_events)
                    data_min = {'Date': [], 'peaks': []}
                    return data, max_events, data_min

                data, max_events = self.__add_peaks(data, max_events)
                data_min = {'Date': [], 'peaks': []}
                return data, max_events, data_min
        else:
            return data, max_events, data_min

    def __test_duration(self, data, max_events):
        data_max = data['Date'][data['peaks'].index(self.__peaks_type_event(data['peaks']))]

        duration_intro_events = data_max - max_events['Date'][-1]
        if duration_intro_events.days < self.duration:
            return True
        return False

    def __test_xmin_bigger_q(self, data, max_events, data_min):
        q1 = max_events['peaks'][-1]
        data_q1 = max_events['Date'][-1]
        q2 = self.__peaks_type_event(data['peaks'])
        data_q2 = data['Date'][data['peaks'].index(q2)]
        df_data = pd.DataFrame(data_min['peaks'], index=data_min['Date'])
        df_data = df_data.loc[data_q1:data_q2]
        if self.type_event == "flood":
            menor = min(q1, q2)
            xmin = df_data.min().values

            if xmin > (3 / 4) * menor:
                return True
            return False
        elif self.type_event == "drought":
            maior = max(q1, q2)
            xmax = df_data.max().values

            if xmax < (3 / 4) * maior:
                return True
            return False
        else:
            return "Type Event Erro!"

    def __test_xmin_bigger_dois_terco_x(self, data, max_events, data_min):
        q1 = max_events['peaks'][-1]
        data_q1 = max_events['Date'][-1]
        q2 = self.__peaks_type_event(data['peaks'])
        data_q2 = data['Date'][data['peaks'].index(q2)]
        df_data = pd.DataFrame(data_min['peaks'], index=data_min['Date'])
        df_data = df_data.loc[data_q1:data_q2]
        if self.type_event == "flood":
            xmin = df_data.min().values
            if xmin < (2 / 3) * q1:
                return True
            return False
        elif self.type_event == "drought":
            xmax = df_data.max().values
            if xmax > (2 / 3) * q1:
                return True
            return False
        else:
            return "Type Event Erro!"

    def test_autocorrelation(self):
        try:
            n = len(self.peaks.peaks)
            serie = pd.Series(self.peaks.peaks, index=self.peaks.index)
            lag1 = serie.autocorr(lag=1)
            lag2 = serie.autocorr(lag=2)
            r11_n = (-1 + 1.645 * math.sqrt(n - 1 - 1)) / (n - 1)
            r12_n = (-1 - 1.645 * math.sqrt(n - 1 - 1)) / (n - 1)
            r21_n = (-1 + 1.645 * math.sqrt(n - 2 - 1)) / (n - 2)
            r22_n = (-1 - 1.645 * math.sqrt(n - 2 - 1)) / (n - 2)
            if r11_n > lag1 > r12_n and r21_n > lag2 > r22_n:
                return False, (r11_n, lag1, r12_n), (r21_n, lag2, r22_n)
            return True, (r11_n, lag1, r12_n), (r21_n, lag2, r22_n)
        except ValueError:
            self.event_peaks()
            self.test_autocorrelation()

    def __troca_peaks(self, data, max_events):

        if max_events['peaks'][-1] < self.__peaks_type_event(data['peaks']):
            max_events['peaks'][-1] = self.__peaks_type_event(data['peaks'])
            max_events['End'][-1] = data['Date'][-1]
            duration = max_events['End'][-1] - max_events['Start'][-1]
            max_events['Duration'][-1] = duration.days
            max_events['Date'][-1] = data['Date'][data['peaks'].index(self.__peaks_type_event(data['peaks']))]
            data = {'Date': list(), 'peaks': list()}
        else:
            max_events['End'][-1] = data['Date'][-1]
            duration = max_events['End'][-1] - max_events['Start'][-1]
            max_events['Duration'][-1] = duration.days
            data = {'Date': list(), 'peaks': list()}
        return data, max_events

    def __add_peaks(self, data, max_events):
        max_events['peaks'].append(self.__peaks_type_event(data['peaks']))
        max_events['Start'].append(data['Date'][0])
        max_events['End'].append(data['Date'][-1])
        duration = max_events['End'][-1] - max_events['Start'][-1]
        max_events['Duration'].append(duration.days)
        max_events['Date'].append(data['Date'][data['peaks'].index(self.__peaks_type_event(data['peaks']))])
        data = {'Date': list(), 'peaks': list()}
        return data, max_events

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

    def hydrogram(self, title, save=False, width=None, height=None, size_text=16, color=None):
        hydrogram = HydrogramParcial(
            data=self.data, peaks=self.peaks,
            threshold=self.threshold, station=self.station,
            threshold_criterion=self.threshold_criterion, title=title, type_criterion=self.type_criterion, width=width,
            height=height, size_text=size_text, color=color)
        fig, data = hydrogram.plot()
        if save:
            aux_name = title.replace(' ', '_')
            py.image.save_as(fig, filename='gráficos/' + '%s.png' % aux_name)

        return fig, data

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

    def polar(self, save=False, width=900, height=900, size_text=14, title=None, color=None, name=None):
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
        if save:
            py.image.save_as(fig, filename='graficos/polar_maximas_anuais.png')

        return fig, data
