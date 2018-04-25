import pandas as pd
import math


class Parcial(object):

    __percentil = 0.8

    def __init__(self, obj, station, type_threshold, value_threshold,
                 type_criterion, type_event):
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
        self.__threshold(self.value)

    def event_peaks(self, duration):
        max_events = {'Data': [], 'Vazao': [], 'Inicio': [], 'Fim': [],
                      'Duracao': []}

        events_criterion = self.__events_over_threshold()[0]
        print(self.threshold)
        events_threshold = self.__events_over_threshold(self.threshold)[0]

        idx_before = events_threshold.index[0]
        low_limiar = False
        data = {'Data': [], 'Vazao': []}
        for i in events_threshold.index:
            boolean, data, max_events = self.__criterion(data=data,
                                                         max_events=max_events,
                                                         duration=duration,
                                                         events_criterion=events_criterion.loc[i])
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

            elif boolean:
                max_events['Vazao'].append(max(data['Vazao']))
                max_events['Inicio'].append(data['Data'][0])
                max_events['Fim'].append(data['Data'][-1])
                max_events['Duracao'].append(len(data['Data']))
                max_events['Data'].append(data['Data'][data['Vazao'].index(max(data['Vazao']))])
                data = {'Data': [], 'Vazao': []}

            idx_before = i

        peaks = pd.DataFrame(max_events,
                            columns=['Duracao', 'Inicio', 'Fim', 'Vazao'],
                            index=max_events['Data'])

        if self.__test_autocorrelation(peaks)[0] and self.type_criterion=='autocorrelação':
            return self.event_peaks(duration=duration+1)
        elif self.__test_threshold_events_by_year(peaks, self.value) and self.type_threshold == 'events_by_year':
            return self.event_peaks(duration=duration)
        return peaks

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
        else:
            self.threshold = self.data[self.station].quantile(value)
        return self.threshold

    def __test_threshold_events_by_year(self, peaks, value):
        n_year = self.obj.date_end.year - self.obj.date_start.year
        print(n_year * value)
        print(len(peaks))
        if len(peaks) < value * n_year:
            self.__percentil -= 0.005
            print(self.__percentil)
            self.__threshold(self.__percentil)
            return True
        return False


    def __criterion(self, *args, **kwargs):
        if self.type_criterion == 'media':
            return self.__criterion_media(data=kwargs['data'],
                                          events_criterion=kwargs['events_criterion']), \
                   kwargs['data'], kwargs['max_events']

        elif self.type_criterion == 'mediana':
            return self.__criterion_mediana(data=kwargs['data'],
                                            events_criterion=kwargs['events_criterion']), \
                   kwargs['data'], kwargs['max_events']

        elif self.type_criterion == 'autocorrelação':
            return self.__criterion_autocorrelation(data=kwargs['data'],
                                                    max_events=kwargs['max_events'],
                                                    duration=kwargs['duration'])

    def __criterion_media(self, data, events_criterion):
        if len(data['Vazao']) > 0 and (not events_criterion):
            return True
        else:
            return False

    def __criterion_mediana(self, data, events_criterion):
        if len(data['Vazao']) > 0 and (not events_criterion):
            return True
        else:
            return False

    def __criterion_autocorrelation(self, data, max_events, duration):
        if len(max_events['Data']) == 0:
            return True, data, max_events
        elif len(data['Data']) == 0:
            return False, data, max_events
        else:
            data_max = data['Data'][data['Vazao'].index(max(data['Vazao']))]
            distancia_dias = data_max - max_events['Data'][-1]
            if distancia_dias.days <= duration:
                if len(data['Vazao']) > 0 and max_events['Vazao'][-1] < max(data['Vazao']):
                    max_events['Vazao'][-1] = max(data['Vazao'])
                    max_events['Fim'][-1] = data['Data'][-1]
                    max_events['Duracao'][-1] = len(data['Data'])
                    max_events['Data'][-1] = data['Data'][data['Vazao'].index(max(data['Vazao']))]
                    data = {'Data': [], 'Vazao': []}
                return False, data, max_events
            return True, data, max_events

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

    def __criterion_duration(self):
        pass
