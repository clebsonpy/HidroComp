import pandas as pd


class Parcial(object):

    def __init__(self, data, station, type_threshold, type_event):
        """
            type_threshold: Type of threshold (stationary or events by year)
        """
        self.data = data
        self.station = station
        self.type_threshold = type_threshold
        self.type_event = type_event

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

    """
    def parcialEventoMediaMaxima(self, tipoEvento):
        limiar = self.maxAnual()[self.nPosto].mean()
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
    """
