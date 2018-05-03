import pandas as pd
import math
import scipy.stats as stat

from comparasion.rmse import RMSE
from comparasion.mae import MAE
from comparasion.genpareto import BootsGenPareto
from graphics.genpareto import GenPareto
from graphics.hydrogram_parcial import HydrogramParcial


class Parcial(object):

    distribution = 'GP'
    __percentil = 0.8
    dic_name = {'stationary': 'Percentil', 'events_by_year': 'Eventos por Ano',
                'autocorrelação': 'Autocorrelacao'}

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
                type_event: Tipo do evento em estudo ('cheia' ou 'estiagem')
        """
        self.obj = obj
        self.data = self.obj.data
        self.station = station
        self.type_threshold = type_threshold
        self.type_criterion = type_criterion
        self.type_event = type_event
        self.value = value_threshold
        self.duration = kwargs['duration']
        self.__threshold(self.value)
        self.name = '%s(%s) - %s' % (self.dic_name[self.type_threshold],
                                     self.value, self.type_criterion.title())

    def event_peaks(self):
        max_events = {'Data': [], 'Vazao': [], 'Inicio': [], 'Fim': [],
                      'Duracao': []}

        events_criterion, self.threshold_criterion = self.__events_over_threshold()
        events_threshold = self.__events_over_threshold(self.threshold)[0]

        idx_before = events_threshold.index[0]
        low_limiar = False

        data = {'Data': [], 'Vazao': []}
        data_min = []
        for i in events_threshold.index:
            if not events_threshold.loc[i] and not low_limiar:
                data_min.append(self.data.loc[idx_before, self.station])

            if events_threshold.loc[i]:
                data['Vazao'].append(self.data.loc[idx_before, self.station])
                data['Data'].append(idx_before)
                low_limiar = True
            elif low_limiar:
                data['Vazao'].append(self.data.loc[idx_before, self.station])
                data['Data'].append(idx_before)
                data['Vazao'].append(self.data.loc[i, self.station])
                data['Data'].append(i)
                low_limiar = False
            else:
                data, max_events, data_min = self.__criterion(data=data,
                                        max_events=max_events,
                                        data_min=data_min,
                                        events_criterion=events_criterion.loc[i])
            idx_before = i

        self.peaks = pd.DataFrame(max_events,
                            columns=['Duracao', 'Inicio', 'Fim', 'Vazao'],
                            index=max_events['Data'])

        if self.type_criterion=='autocorrelação' and self.__test_autocorrelation(self.peaks)[0]:
            self.duration += 1
            return self.event_peaks()
        elif self.type_threshold == 'events_by_year' and \
                self.__test_threshold_events_by_year(self.peaks, self.value):
            return self.event_peaks()
        return self.peaks

    def __events_over_threshold(self, threshold=None):
        if threshold is None:
            if self.type_criterion == 'media':
                threshold = self.data[self.station].mean()
            elif self.type_criterion == 'mediana':
                threshold = self.data[self.station].median()

        if self.type_event == 'cheia':
            events = self.data[self.station].isin(self.data.loc[self.data[
                self.station] >= threshold, self.station])
            return events, threshold

        elif self.type_event == 'estiagem':
            events = self.data[self.station].isin(self.data.loc[self.data[
                self.station] <= threshold, self.station])
            return events, threshold

        else:
            return 'Evento erro!'

    def __threshold(self, value):
        if value > 1 and self.type_threshold == 'events_by_year':
            self.threshold = self.data[self.station].quantile(self.__percentil)
        elif value > 1 and self.type_threshold == 'stationary':
            self.threshold = value
        elif self.type_threshold == 'autocorrelação':
            self.threshold = self.data[self.station].quantile(self.__percentil)
        else:
            self.threshold = self.data[self.station].quantile(self.__percentil)
        return self.threshold

    def __test_threshold_events_by_year(self, peaks = None, value = None):
        n_year = self.obj.date_end.year - self.obj.date_start.year
        if self.type_criterion == 'events_by_year':
            if len(peaks) < int(value * n_year):
                self.__percentil -= 0.005
                self.__threshold(self.__percentil)
                return True
            elif len(peaks) > (int(value * n_year)+3):
                self.__percentil += 0.005
                self.__threshold(self.__percentil)
                return True
            return False
        if self.type_threshold == 'autocorrelação':
            self.__percentil -= 0.005
            self.__threshold(self.__percentil)

    def __criterion(self, *args, **kwargs):
        if self.type_criterion == 'media':
            data, max_events = self.__criterion_media(data=kwargs['data'],
                                    max_events=kwargs['max_events'],
                                    events_criterion=kwargs['events_criterion'])
            return data, max_events, kwargs['data_min']

        elif self.type_criterion == 'mediana':
            data, max_events = self.__criterion_mediana(data=kwargs['data'],
                                    max_events=kwargs['max_events'],
                                    events_criterion=kwargs['events_criterion'])
            return data, max_events, kwargs['data_min']

        elif self.type_criterion == 'autocorrelação':
            data, max_events = self.__criterion_duration(data=kwargs['data'],
                                    max_events=kwargs['max_events'],
                                    events_criterion=kwargs['events_criterion'])
            return data, max_events, kwargs['data_min']

        elif self.type_criterion == 'xmin_maior_qmin':
            return self.__criterion_xmin_maior_qmin(data=kwargs['data'],
                             max_events=kwargs['max_events'],
                             data_min=kwargs['data_min'],
                             events_criterion=kwargs['events_criterion'])

        elif self.type_criterion == 'xmin_maior_dois_terco_x':
            return self.__criterion_xmin_maior_dois_terco(data=kwargs['data'],
                                    max_events=kwargs['max_events'],
                                    data_min=kwargs['data_min'],
                                    events_criterion=kwargs['events_criterion'])

        elif self.type_criterion == 'duracao_e_xmin':
            return self.__criterion_duration_and_xmin(data=kwargs['data'],
                                    max_events=kwargs['max_events'],
                                    data_min=kwargs['data_min'],
                                    events_criterion=kwargs['events_criterion'])

    def __criterion_media(self, data, max_events, events_criterion):
        if len(data['Vazao']) > 0 and (not events_criterion):
            return self.__add_peaks(data, max_events)
        else:
            return data, max_events

    def __criterion_mediana(self, data, max_events, events_criterion):
        if len(data['Vazao']) > 0 and (not events_criterion):
            return self.__add_peaks(data, max_events)
        else:
            return data, max_events

    def __criterion_duration(self, data, max_events, events_criterion):
        if not events_criterion:
            if len(data['Data']) == 0:
                return data, max_events
            elif len(max_events['Data']) == 0:
                return self.__add_peaks(data, max_events)
            else:
                if self.__test_duration(data, max_events):
                    data, max_events = self.__troca_peaks(data, max_events)
                    return data, max_events
                return self.__add_peaks(data, max_events)
        else:
            return data, max_events

    def __criterion_xmin_maior_qmin(self, data, max_events, data_min, events_criterion):
        if not events_criterion:
            if len(data['Data']) == 0:
                return data, max_events, data_min
            elif len(max_events['Data']) == 0:
                data, max_events = self.__add_peaks(data, max_events)
                data_min = []
                return data, max_events, data_min
            elif len(data_min) == 0:
                return data, max_events, data_min
            else:
                if self.__test_xmin_maior_q(data, max_events, data_min):
                    data, max_events = self.__troca_peaks(data, max_events)
                    data_min = []
                    return data, max_events, data_min
                data, max_events = self.__add_peaks(data, max_events)
                data_min = []
                return data, max_events, data_min
        else:
            return data, max_events, data_min

    def __criterion_xmin_maior_dois_terco_x(self, data, max_events, data_min,
                                          events_criterion):
        if not events_criterion:
            if len(data['Data']) == 0:
                return data, max_events, data_min
            elif len(max_events['Data']) == 0:
                data, max_events = self.__add_peaks(data, max_events)
                data_min = []
                return data, max_events, data_min
            elif len(data_min) == 0:
                return data, max_events, data_min
            else:
                if self.__test_xmin_maior_dois_terco_x(data, max_events, data_min):
                    data, max_events = self.__troca_peaks(data, max_events)
                    data_min = []
                    return data, max_events, data_min
                data, max_events = self.__add_peaks(data, max_events)
                data_min = []
                return data, max_events, data_min
        else:
            return data, max_events, data_min

    def __criterion_duration_and_xmin(self, data, max_events, events_criterion,
                                      data_min):
        if not events_criterion:
            if len(data['Data']) == 0:
                return data, max_events, data_min
            elif len(max_events['Data']) == 0:
                data, max_events = self.__add_peaks(data, max_events)
                data_min = []
                return data, max_events, data_min
            elif len(data_min) == 0:
                return data, max_events, data_min
            else:
                if self.__test_xmin_maior_q(data, max_events, data_min) or \
                   self.__test_duration(data, max_events):
                    data, max_events = self.__troca_peaks(data, max_events)
                    data_min = []
                    return data, max_events, data_min

                data, max_events = self.__add_peaks(data, max_events)
                data_min = []
                return data, max_events, data_min
        else:
            return data, max_events, data_min

    def __test_duration(self, data, max_events):
        data_max = data['Data'][data['Vazao'].index(max(data['Vazao']))]
        distancia_dias = data_max - max_events['Data'][-1]
        if distancia_dias.days < self.duration:
            return True
        return False

    def __test_xmin_maior_q(self, data, max_events, data_min):
        q1 = max_events['Vazao'][-1]
        q2 = max(data['Vazao'])
        menor = min(q1, q2)
        xmin = min(data_min)
        if xmin > (3/4)*menor:
            return True
        return False

    def __test_xmin_maior_dois_terco_x(self, data, max_events, data_min):
        xmin = min(data_min)
        q = max_events['Vazao'][-1]
        if xmin > (2/3)*q:
            return True
        return False

    def __test_autocorrelation(self, events_peaks):
        x = events_peaks.index
        y = events_peaks.Vazao
        N = len(y)
        serie = pd.Series(y, index=x)
        r1 = serie.autocorr(lag=1)
        r2 = serie.autocorr(lag=2)
        r11_n = (-1 + 1.645 * math.sqrt(N - 1 - 1)) / (N - 1)
        r12_n = (-1 - 1.645 * math.sqrt(N - 1 - 1)) / (N - 1)
        r21_n = (-1 + 1.645 * math.sqrt(N - 2 - 1)) / (N - 2)
        r22_n = (-1 - 1.645 * math.sqrt(N - 2 - 1)) / (N - 2)

        if r11_n > r1 > r12_n and r21_n > r2 > r22_n:
            return False, r1, r2
        return True, r1, r2

    def __troca_peaks(self, data, max_events):

        if max_events['Vazao'][-1] < max(data['Vazao']):
            max_events['Vazao'][-1] = max(data['Vazao'])
            max_events['Fim'][-1] = data['Data'][-1]
            duration = max_events['Fim'][-1] - max_events['Inicio'][-1]
            max_events['Duracao'][-1] = duration.days
            max_events['Data'][-1] = data['Data'][data['Vazao'].index(max(data['Vazao']))]
            data = {'Data': [], 'Vazao': []}
        else:
            max_events['Fim'][-1] = data['Data'][-1]
            duration = max_events['Fim'][-1] - max_events['Inicio'][-1]
            max_events['Duracao'][-1] = duration.days
            data = {'Data': [], 'Vazao': []}

        return data, max_events

    def __add_peaks(self, data, max_events):
        max_events['Vazao'].append(max(data['Vazao']))
        max_events['Inicio'].append(data['Data'][0])
        max_events['Fim'].append(data['Data'][-1])
        duration = max_events['Fim'][-1] - max_events['Inicio'][-1]
        max_events['Duracao'].append(duration.days)
        max_events['Data'].append(data['Data'][data['Vazao'].index(max(data['Vazao']))])
        data = {'Data': [], 'Vazao': []}
        return data, max_events

    def mvs(self):
        try:
            self.para = stat.genpareto.fit(self.peaks['Vazao'].values)
        except AttributeError:
            self.event_peaks()
            self.para = stat.genpareto.fit(self.peaks['Vazao'].values)

        return self.para

    def resample(self, quantidade):
        try:
            n = len(self.peaks)
            df_resample = pd.DataFrame()
            for i in range(quantidade):
                df = pd.DataFrame(self.peaks['Vazao'].sample(n=n, replace=True).values,
                                    columns=['%s' % i])
                df_resample = df_resample.combine_first(df)
            return df_resample
        except AttributeError:
            self.event_peaks()
            return self.resample(quantidade)

    def mvs_resample(self, quantidade):
        dic = {'Parametro': []}
        resample = self.resample(quantidade)
        peaks = self.peaks.copy()
        for i in resample:
            self.peaks['Vazao'] = resample[i].values
            dic['Parametro'].append(self.mvs())
        self.peaks = peaks
        return pd.DataFrame(dic)

    def magnitude(self, tempo_de_retorno):
        try:
            if type(tempo_de_retorno) is list:
                raise TypeError
            try:
                prob = 1-(1/tempo_de_retorno)
                mag = stat.genpareto.ppf(prob, self.para[0], self.para[1],
                                         self.para[2])
            except AttributeError:
                self.mvs()
                self.magnitude(tempo_de_retorno)
        except TypeError:
            mag = self.__magnitudes(tempo_de_retorno)
        return mag

    def __magnitudes(self, tempo_de_retorno, name=None):
        #dic_magns = {0.001:[], 0.01:[], 0.1:[], 0.5:[], 0.9:[], 0.99:[], 0.999:[]}
        if name is None:
            name = self.name

        magns = []
        for tempo in tempo_de_retorno:
            mag = self.magnitude(tempo)
            #mag = stat.genpareto.ppf(j, self.para[0], self.para[1],
            #                         self.para[2])

            magns.append(mag)

        return pd.Series(magns, index=tempo_de_retorno, name=name)

    def magnitude_resample(self, quantidade, tempo_de_retorno):
        df_magn = pd.DataFrame()
        para = self.mvs_resample(quantidade)
        para_origon = self.mvs()
        print(self.para)
        for i in para.index:
            self.para = para['Parametro'][i]
            serie = self.__magnitudes(tempo_de_retorno, i)
            df_magn = df_magn.combine_first(serie.to_frame())

        self.para = para_origon
        return df_magn.T

    def plot_distribution(self, title, type_function):
        try:
            genpareto = GenPareto(title, self.para[0], self.para[1], self.para[2])
            return genpareto.plot(type_function), self.para
        except AttributeError:
            self.mvs()
            self.plot_distribution(title, type_function)

    def plot_hydrogram(self, title):
        try:
            hydrogrm = HydrogramParcial(data=self.data[self.station],
                                        peaks=self.peaks,
                                        threshold=self.threshold,
                                        threshold_criterion=self.threshold_criterion,
                                        title = title)
            hydrogrm.plot(type_criterion=self.type_criterion)
        except AttributeError:
            self.event_peaks()
            self.plot_hydrogram(title)
