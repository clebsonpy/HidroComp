import pandas as pd
import math
import scipy.stats as stat
import plotly.plotly as py

from graphics.genpareto import GenPareto
from graphics.hydrogram_parcial import HydrogramParcial
from graphics.boxplot import Boxplot


class Parcial(object):

    distribution = 'GP'
    __percentil = 0.8
    dic_name = {'stationary': 'Percentil', 'events_by_year': 'Eventos por Ano',
                'autocorrelation': 'Autocorrelação'}

    def __init__(self, obj, station, type_threshold, value_threshold,
                 type_criterion, type_event, **kwargs):
        """
            Parâmetros:
                obj: Objeto Série;
                station: Ponto de observação dos dados('XINGO')
                type_threshold: Tipo de calculo do limiar('stationary' ou
                                                          'events_by_year')
                value_threshold: Valor do limiar:
                    Para type_threshold = 'stationary': percentil ou valor
                    Para type_threshold = 'events_by_year': quantidade média de
                                                            picos por ano
                type_criterion: Critério de Independência ('media', 'mediana')
                type_event: Tipo do evento em estudo ('flood' ou 'drought')
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
        self.duration = kwargs['duration']
        if type_criterion == 'median':
            self.__percentil = 0.65

        self.__threshold(self.value)
        self.name = '%s(%s) - %s' % (self.dic_name[self.type_threshold],
                                     self.value, self.type_criterion.title())

    def event_peaks(self):
        max_events = {'Date': list(), 'Flow': list(), 'Start': list(), 'End': list(),
                      'Duration': list()}

        events_criterion, self.threshold_criterion = self.__events_over_threshold()
        events_threshold = self.__events_over_threshold(self.threshold)[0]

        idx_before = events_threshold.index[0]
        low_limiar = False

        data = {'Date': list(), 'Flow': list()}
        data_min = {'Date': list(), 'Flow': list()}

        for i in events_threshold.index:
            if not events_threshold.loc[i] and not low_limiar:
                data_min['Flow'].append(self.data.loc[idx_before, self.station])
                data_min['Date'].append(idx_before)

            if events_threshold.loc[i]:
                data['Flow'].append(self.data.loc[idx_before, self.station])
                data['Date'].append(idx_before)
                low_limiar = True
                data_min['Flow'].append(self.data.loc[idx_before, self.station])
                data_min['Date'].append(idx_before)
            elif low_limiar:
                data['Flow'].append(self.data.loc[idx_before, self.station])
                data['Date'].append(idx_before)
                data['Flow'].append(self.data.loc[i, self.station])
                data['Date'].append(i)
                low_limiar = False
                data_min['Flow'].append(self.data.loc[idx_before, self.station])
                data_min['Date'].append(idx_before)
            else:
                data, max_events, data_min = self.__criterion(
                    data=data, max_events=max_events, data_min=data_min,
                    events_criterion=events_criterion.loc[i]
                )
            idx_before = i

        self.peaks = pd.DataFrame(
            max_events, columns=['Duration', 'Start', 'End', 'Flow'],
            index=max_events['Date']
        )

        if (self.type_criterion == 'autocorrelation'
                and self.__test_autocorrelation(self.peaks)[0]):
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

        if self.type_event == 'flood':
            events = self.data[self.station].isin(self.data.loc[self.data[
                self.station] >= threshold, self.station])
            return events, threshold

        elif self.type_event == 'drought':
            events = self.data[self.station].isin(self.data.loc[self.data[
                self.station] <= threshold, self.station])
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

        if len(peaks)+1 < int(value * n_year):
            self.__percentil -= 0.005
            self.__threshold(self.__percentil)
            return True
        elif len(peaks) > (int(value * n_year)+2):
            self.__percentil += 0.005
            self.__threshold(self.__percentil)
            return True
        return False

    def __criterion(self, **kwargs):
        if self.type_criterion == 'mean':
            data, max_events = self.__criterion_mean(
                data=kwargs['data'], max_events=kwargs['max_events'],
                events_criterion=kwargs['events_criterion']
            )
            return data, max_events, kwargs['data_min']

        elif self.type_criterion == 'median':
            data, max_events = self.__criterion_median(
                data=kwargs['data'], max_events=kwargs['max_events'],
                events_criterion=kwargs['events_criterion']
            )
            return data, max_events, kwargs['data_min']

        elif self.type_criterion == 'autocorrelation':
            data, max_events = self.__criterion_duration(
                data=kwargs['data'], max_events=kwargs['max_events'],
                events_criterion=kwargs['events_criterion']
            )
            return data, max_events, kwargs['data_min']

        elif self.type_criterion == 'xmin_bigger_qmin':
            return self.__criterion_xmin_bigger_qmin(
                data=kwargs['data'], max_events=kwargs['max_events'],
                data_min=kwargs['data_min'],
                events_criterion=kwargs['events_criterion']
            )

        elif self.type_criterion == 'xmin_bigger_dois_terco_x':
            return self.__criterion_xmin_bigger_dois_terco_x(
                data=kwargs['data'], max_events=kwargs['max_events'],
                data_min=kwargs['data_min'],
                events_criterion=kwargs['events_criterion']
            )

        elif self.type_criterion == 'duration_e_xmin':
            return self.__criterion_duration_and_xmin(
                data=kwargs['data'], max_events=kwargs['max_events'],
                data_min=kwargs['data_min'],
                events_criterion=kwargs['events_criterion']
            )

    def __criterion_mean(self, data, max_events, events_criterion):
        if len(data['Flow']) > 0 and (not events_criterion):
            return self.__add_peaks(data, max_events)
        else:
            return data, max_events

    def __criterion_median(self, data, max_events, events_criterion):
        if len(data['Flow']) > 0 and (not events_criterion):
            return self.__add_peaks(data, max_events)
        else:
            return data, max_events

    def __criterion_duration(self, data, max_events, events_criterion):
        if not events_criterion:
            if len(data['Flow']) == 0:
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

    def __criterion_xmin_bigger_qmin(self, data, max_events, data_min,
                                     events_criterion):
        if not events_criterion:
            if len(data['Date']) == 0:
                return data, max_events, data_min
            elif len(max_events['Date']) == 0:
                data, max_events = self.__add_peaks(data, max_events)
                data_min = {'Date': [], 'Flow': []}
                return data, max_events, data_min
            elif len(data_min) == 0:
                return data, max_events, data_min
            else:
                if self.__test_xmin_bigger_q(data, max_events, data_min):
                    data, max_events = self.__troca_peaks(data, max_events)
                    data_min = {'Date': [], 'Flow': []}
                    return data, max_events, data_min
                data, max_events = self.__add_peaks(data, max_events)
                data_min = {'Date': [], 'Flow': []}
                return data, max_events, data_min
        else:
            return data, max_events, data_min

    def __criterion_xmin_bigger_dois_terco_x(self, data, max_events, data_min,
                                             events_criterion):
        if not events_criterion:
            if len(data['Date']) == 0:
                return data, max_events, data_min
            elif len(max_events['Date']) == 0:
                data, max_events = self.__add_peaks(data, max_events)
                data_min = {'Date': [], 'Flow': []}
                return data, max_events, data_min
            elif len(data_min) == 0:
                return data, max_events, data_min
            else:
                if self.__test_xmin_bigger_dois_terco_x(data, max_events, data_min):
                    data, max_events = self.__troca_peaks(data, max_events)
                    data_min = {'Date': [], 'Flow': []}
                    return data, max_events, data_min
                data, max_events = self.__add_peaks(data, max_events)
                data_min = {'Date': [], 'Flow': []}
                return data, max_events, data_min
        else:
            return data, max_events, data_min

    def __criterion_duration_and_xmin(self, data, max_events, events_criterion,
                                      data_min):
        if not events_criterion:
            if len(data['Date']) == 0:
                return data, max_events, data_min
            elif len(max_events['Date']) == 0:
                data, max_events = self.__add_peaks(data, max_events)
                data_min = {'Date': [], 'Flow': []}
                return data, max_events, data_min
            elif len(data_min) == 0:
                return data, max_events, data_min
            else:
                if self.__test_xmin_bigger_q(data, max_events, data_min) or \
                   self.__test_duration(data, max_events):
                    data, max_events = self.__troca_peaks(data, max_events)
                    data_min = {'Date': [], 'Flow': []}
                    return data, max_events, data_min

                data, max_events = self.__add_peaks(data, max_events)
                data_min = {'Date': [], 'Flow': []}
                return data, max_events, data_min
        else:
            return data, max_events, data_min

    def __test_duration(self, data, max_events):
        data_max = data['Date'][data['Flow'].index(
            self.__peaks_type_event(data['Flow']))]

        distancia_dias = data_max - max_events['Date'][-1]
        if distancia_dias.days < self.duration:
            return True
        return False

    def __test_xmin_bigger_q(self, data, max_events, data_min):
        q1 = max_events['Flow'][-1]
        data_q1 = max_events['Date'][-1]
        q2 = self.__peaks_type_event(data['Flow'])
        data_q2 = data['Date'][data['Flow'].index(q2)]
        df_data = pd.DataFrame(data_min['Flow'], index=data_min['Date'])
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
        q1 = max_events['Flow'][-1]
        data_q1 = max_events['Date'][-1]
        q2 = self.__peaks_type_event(data['Flow'])
        data_q2 = data['Date'][data['Flow'].index(q2)]
        df_data = pd.DataFrame(data_min['Flow'], index=data_min['Date'])
        df_data = df_data.loc[data_q1:data_q2]
        if self.type_event == "flood":
            xmin = df_data.min().values
            if xmin > (2 / 3) * q1:
                return True
            return False
        elif self.type_event == "drought":
            xmax = df_data.max().values
            if xmax < (2 / 3) * q1:
                return True
            return False
        else:
            return "Type Event Erro!"

    def __test_autocorrelation(self, events_peaks):
        x = events_peaks.index
        y = events_peaks.Vazao
        n = len(y)
        serie = pd.Series(y, index=x)
        r1 = serie.autocorr(lag=1)
        r2 = serie.autocorr(lag=2)
        r11_n = (-1 + 1.645 * math.sqrt(n - 1 - 1)) / (n - 1)
        r12_n = (-1 - 1.645 * math.sqrt(n - 1 - 1)) / (n - 1)
        r21_n = (-1 + 1.645 * math.sqrt(n - 2 - 1)) / (n - 2)
        r22_n = (-1 - 1.645 * math.sqrt(n - 2 - 1)) / (n - 2)

        if r11_n > r1 > r12_n and r21_n > r2 > r22_n:
            return False, r1, r2
        return True, r1, r2

    def __troca_peaks(self, data, max_events):

        if max_events['Flow'][-1] < self.__peaks_type_event(data['Flow']):
            max_events['Flow'][-1] = self.__peaks_type_event(data['Flow'])
            max_events['End'][-1] = data['Date'][-1]
            duration = max_events['End'][-1] - max_events['Start'][-1]
            max_events['Duration'][-1] = duration.days
            max_events['Date'][-1] = data['Date'][
                data['Flow'].index(self.__peaks_type_event(data['Flow']))
            ]
            data = {'Date': list(), 'Flow': list()}
        else:
            max_events['End'][-1] = data['Date'][-1]
            duration = max_events['End'][-1] - max_events['Start'][-1]
            max_events['Duration'][-1] = duration.days
            data = {'Date': list(), 'Flow': list()}

        return data, max_events

    def __add_peaks(self, data, max_events):
        max_events['Flow'].append(self.__peaks_type_event(data['Flow']))
        max_events['Start'].append(data['Date'][0])
        max_events['End'].append(data['Date'][-1])
        duration = max_events['End'][-1] - max_events['Start'][-1]
        max_events['Duration'].append(duration.days)
        max_events['Date'].append(data['Date'][
                data['Flow'].index(self.__peaks_type_event(data['Flow']))])

        data = {'Date': list(), 'Flow': list()}
        return data, max_events

    def mvs(self):
        try:
            self.fit = stat.genpareto.fit(self.peaks['Flow'].values)
        except AttributeError:
            self.event_peaks()
            self.fit = stat.genpareto.fit(self.peaks['Flow'].values)

        return self.fit

    def resample(self, quantity):
        try:
            n = len(self.peaks)
            df_resample = pd.DataFrame()
            for i in range(quantity):
                df = pd.DataFrame(
                    self.peaks['Flow'].sample(n=n, replace=True).values,
                    columns=['%s' % i]
                )
                df_resample = df_resample.combine_first(df)
            return df_resample

        except AttributeError:
            self.event_peaks()
            return self.resample(quantity)

    def mvs_resample(self, quantity):
        dic = {'Parameter': list()}
        resample = self.resample(quantity)
        peaks = self.peaks.copy()
        for i in resample:
            self.peaks['Flow'] = resample[i].values
            dic['Parameter'].append(self.mvs())
        self.peaks = peaks
        return pd.DataFrame(dic)

    def magnitude(self, return_period):
        try:
            if type(return_period) is list:
                raise TypeError
            try:
                prob = 1-(1 / return_period)
                mag = stat.genpareto.ppf(prob, self.fit[0], self.fit[1],
                                         self.fit[2])
                return mag

            except AttributeError:
                self.mvs()
                return self.magnitude(return_period)

        except TypeError:
            mag = self.__magnitudes(return_period)
            return mag

    def __magnitudes(self, return_periods, name=None):
        if name is None:
            name = self.name

        magns = list()
        for return_period in return_periods:
            mag = self.magnitude(return_period)

            magns.append(mag)

        return pd.Series(magns, index=return_periods, name=name)

    def magnitude_resample(self, quantity, return_period):
        magn = pd.DataFrame()
        para = self.mvs_resample(quantity)
        fit_origin = self.mvs()
        for i in para.index:
            self.fit = para['Parameter'][i]
            serie = self.__magnitudes(return_period, i)
            magn = magn.combine_first(serie.to_frame())

        self.fit = fit_origin
        magn_resample = magn.T
        return magn_resample

    def plot_distribution(self, title, type_function, save=False):
        try:
            genpareto = GenPareto(title, self.fit[0], self.fit[1], self.fit[2])
            data, fig = genpareto.plot(type_function)
            if save:
                aux_name = title.replace(' ', '_')
                py.image.save_as(fig, filename='gráficos/'+'%s.png' % aux_name)
            return data, fig
        except AttributeError:
            self.mvs()
            return self.plot_distribution(title, type_function)

    def plot_hydrogram(self, title, save=False):
        try:
            hydrogram = HydrogramParcial(
                data=self.data[self.station], peaks=self.peaks,
                threshold=self.threshold,
                threshold_criterion=self.threshold_criterion, title=title)
            data, fig = hydrogram.plot(type_criterion=self.type_criterion)
            if save:
                aux_name = title.replace(' ', '_')
                py.image.save_as(fig, filename='gráficos/'+'%s.png' % aux_name)

            return data, fig
        except AttributeError:
            self.event_peaks()
            return self.plot_hydrogram(title)

    def plot_boxplot_resample(self, magn_resample, name, save=False):

        data, fig = Boxplot(magn_resample=magn_resample, name=name).plot()
        if save:
            py.image.save_as(fig, filename='gráficos/boxplot_%s.png' % name)

        return data, fig
