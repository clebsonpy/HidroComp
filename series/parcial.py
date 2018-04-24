import pandas as pd
import math


class Parcial(object):

    def __init__(self, data, station, type_threshold, value_threshold,
                 type_criterion, type_event):
        """
            type_threshold: Type of threshold (stationary or events by year)
        """
        self.data = data
        self.station = station
        self.type_threshold = type_threshold
        self.type_criterion = type_criterion
        self.type_event = type_event
        self.threshold(value_threshold)

    def event_peaks(self, duration):
        max_events = {'Data': [], 'Vazao': [], 'Inicio': [], 'Fim': [],
                      'Duracao': []}

        events = self.__events_over_threshold(self.threshold)
        idx_before = events.index[0]
        low_limiar = False
        data = {'Data': [], 'Vazao': []}
        for i in events.index:
            boolean, data, max_events = self.__criterion(data=data, idx=i,
                                                         max_events=max_events,
                                                         duration=duration)
            if events.loc[i]:
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
        return peaks

    def __events_over_threshold(self, threshold):
        if self.type_event == 'cheia':
            events = self.data[self.station].isin(self.data.loc[self.data[
                self.station] >= threshold, self.station])
            return events

        elif self.type_event == 'estiagem':
            events = self.data[self.station].isin(self.data.loc[self.data[
                self.station] <= threshold, self.station])
            return events

        else:
            return 'Evento erro!'

    def threshold(self, value):
        if self.type_threshold == 'stationary' and value > 0:
            return self.__threshold_stationary(value)
        elif self.type_threshold == 'events_by_year' and value > 0:
            return self.__threshold_events_by_year(value)

    def __threshold_stationary(self, value):
        if value > 1:
            self.threshold = value
        else:
            self.threshold = self.data[self.station].quantile(value)

        return self.threshold

    def __threshold_events_by_year(self, value):
        pass

    def __criterion(self, *args, **kwargs):
        if self.type_criterion == 'media':
            return self.__criterion_media(data=kwargs['data'],
                                          idx=kwargs['idx']), kwargs['data'], kwargs['max_events']
        elif self.type_criterion == 'mediana':
            return self.__criterion_mediana(data=kwargs['data'],
                                            idx=kwargs['idx']), kwargs['data'], kwargs['max_events']
        elif self.type_criterion == 'autocorrelação':
            return self.__criterion_autocorrelation(data=kwargs['data'],
                                                    max_events=kwargs['max_events'],
                                                    duration=kwargs['duration'])

    def __criterion_media(self, data, idx):
        mean = self.data[self.station].mean()
        events = self.__events_over_threshold(mean)
        if len(data['Vazao']) > 0 and (not events.loc[idx]):
            return True
        else:
            return False

    def __criterion_mediana(self, data, idx):
        median = self.data[self.station].median()
        events = self.__events_over_threshold(median)
        if len(data['Vazao']) > 0 and (not events.loc[idx]):
            return True
        else:
            return False

    def auto(self):
        pass

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
