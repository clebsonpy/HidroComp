import pandas as pd


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

        events = self.events_over_threshold()
        idx_before = events.index[1]
        low_limiar = False
        data = {'Data': [], 'Vazao': []}
        for i in events.index:
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

            elif self.__criterion(data=data, idx=i, max_events=max_events,
                                  duration=duration):
                max_events['Vazao'].append(max(data['Vazao']))
                max_events['Inicio'].append(data['Data'][0])
                max_events['Fim'].append(data['Data'][-1])
                max_events['Duracao'].append(len(data['Data']))
                max_events['Data'].append(data['Data'][data['Vazao'].index(max(data['Vazao']))])
                data = {'Data': [], 'Vazao': []}
            """
            elif dias > 0 and len(dados['Vazao']) > 0 and max_evento['Vazao'][-1] < max(dados['Vazao']):
                max_evento['Ano'][-1] = key.year
                max_evento['Vazao'][-1] = max(dados['Vazao'])
                max_evento['Fim'][-1] = dados['Data'][-1]
                max_evento['Duracao'][-1] = len(dados['Data'])
                max_evento['Data'][-1] = dados['Data'][dados['Vazao'].index(max(dados['Vazao']))]
                dados = {'Data': [], 'Vazao': []}
            """
            idx_before = i
        return pd.DataFrame(max_events,
                            columns=['Duracao', 'Inicio', 'Fim', 'Vazao'],
                            index=max_events['Data'])

    def events_over_threshold(self):
        if self.type_event == 'cheia':
            events = self.data[self.station].isin(self.data.loc[self.data[
                self.station] >= self.threshold, self.station])
            return events

        elif self.type_event == 'estiagem':
            events = self.data[self.station].isin(self.data.loc[self.data[
                self.station] <= self.threshold, self.station])
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
            return self.__criterion_media(data=kwargs['data'], idx=kwargs['idx'])
        elif self.type_criterion == 'mediana':
            return self.__criterion_mediana(data, idx)

    def __criterion_media(self, data, idx):
        mean = self.data[self.station].mean()
        if self.type_event == 'cheia':
            event_parcial = self.data[self.station].isin(self.data.loc[
                self.data[self.station] >= mean, self.station])
        elif self.type_event == 'estiagem':
            event_parcial = self.data[self.station].isin(self.data.loc[
                self.data[self.station] <= mean, self.station])

        if len(data['Vazao']) > 0 and (not event_parcial.loc[idx]):
            return True
        else:
            return False

    def __criterion_mediana(self):
        pass

    def __criterion_autocorrelation(self):
        pass

    def __criterion_duration(self):
        pass






    """
    def parcialEventoPorAno(self, limiar, tipoEvento):
        if tipoEvento == 'cheia':
            eventoL = self.dadosVazao[self.nPosto].isin(
                self.dadosVazao.loc[self.dadosVazao[self.nPosto] >= limiar, self.nPosto])
            return eventoL
        elif tipoEvento == 'estiagem':
            eventoL = self.dadosVazao[self.nPosto].isin(
                self.dadosVazao.loc[self.dadosVazao[self.nPosto] <= limiar, self.nPosto])
            return eventoL
        else:
            return 'Evento erro!'

    def parcialPorAno(self, nEventos, tipoEvento):
        nAnos = self.dadosVazao[self.nPosto].index.year[-1] - \
            self.dadosVazao[self.nPosto].index.year[0]
        l = self.dadosVazao[self.nPosto].quantile(0.7)
        #vazao = -np.sort(-self.dadosVazao.loc[self.dadosVazao[self.nPosto] <= l, self.nPosto])
        q = 0.8
        while q != 0:
            limiar = self.dadosVazao[self.nPosto].quantile(q)
            print(limiar)
            eventosL = self.parcialEventoPorAno(limiar, tipoEvento)
            picos = self.eventos_picos(eventosL, tipoEvento)
            print(len(picos), nEventos * nAnos)
            if len(picos) >= nEventos * nAnos:
                return picos, limiar
            q -= 0.005

    def parcialEventoPercentil(self, quartilLimiar, tipoEvento):
        limiar = self.dadosVazao[self.nPosto].quantile(quartilLimiar)
        if tipoEvento == 'cheia':
            eventoL = self.dadosVazao[self.nPosto].isin(
                self.dadosVazao.loc[self.dadosVazao[self.nPosto] >= limiar, self.nPosto])
            return eventoL, limiar
        elif tipoEvento == 'estiagem':
            eventoL = self.dadosVazao[self.nPosto].isin(
                self.dadosVazao.loc[self.dadosVazao[self.nPosto] <= limiar, self.nPosto])
            return eventoL, limiar
        else:
            return 'Evento erro!'

    def __criterioMedia(self, dados, index, tipoEvento):
        mean = self.dadosVazao[self.nPosto].mean()
        if tipoEvento == 'cheia':
            eventos = self.dadosVazao[self.nPosto].isin(
                self.dadosVazao.loc[self.dadosVazao[self.nPosto] >= mean, self.nPosto])
        elif tipoEvento == 'estiagem':
            eventos = self.dadosVazao[self.nPosto].isin(
                self.dadosVazao.loc[self.dadosVazao[self.nPosto] <= mean, self.nPosto])

        if len(dados['Vazao']) > 0 and (not eventos.loc[index] or
                                        index == pd.to_datetime("%s0831" % index.year)):
            return True
        else:
            return False
    """
