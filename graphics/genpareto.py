import scipy.stats as stat
import pandas as pd

import plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF
import colorlover as cl
import cufflinks as cf

from graphics.distribution_biuld import DistributionBiuld


class GenPareto(DistributionBiuld):

    def __init__(self, title, forma, localizacao, escala):
        super().__init__(title, forma, localizacao, escala)

    def cumulative(self):
        dados = self._data('cumulative')
        data = go.Scatter(x=dados['Vazao'], y=dados['Probabilidade'],
                          name=self.title.title())
        data_fig = [data]

        bandxaxis = go.XAxis(title="Vazão(m³/s)")
        bandyaxis = go.YAxis(title="Probabilidade")

        layout = dict(title="GP - Acumulada: %s" % self.title.title(),
                      xaxis=bandxaxis,
                      width=840, height=672,
                      yaxis=bandyaxis,
                      font=dict(family='Courier New, monospace', size=16,
                                color='#7f7f7f'))

        fig = dict(data=data_fig, layout=layout)
        name_graphic = 'GP_Acumulada_%s' % self.title
        py.offline.plot(fig, filename='gráficos/'+ name_graphic + '.html')

        return data

    def density(self):
        dados = self._data('density')
        data = go.Scatter(x=dados['Vazao'], y=dados['Densidade'],
                          name=self.title.title())
        data_fig = [data]

        bandxaxis = go.XAxis(title="Vazão(m³/s)")
        bandyaxis = go.YAxis(title="Densidade")

        layout = dict(title="GP - Densidade: %s" % self.title.title(),
                      xaxis=bandxaxis, width=840,
                      height=672, yaxis=bandyaxis,
                      font=dict(family='Courier New, monospace', size=16,
                                color='#7f7f7f'))

        fig = dict(data=data_fig, layout=layout)
        name_graphic = 'GP_Densidade_%s' % self.title
        py.offline.plot(fig, filename='gráficos/'+ name_graphic + '.html')

        return data

    def _data_density(self):

        cumulative = self._data_cumulative()
        density = stat.genpareto.pdf(cumulative['Vazao'].values, self.forma,
                                 loc=self.localizacao, scale=self.escala)

        dic = {'Vazao': cumulative['Vazao'].values, 'Densidade': density}

        return pd.DataFrame(dic)

    def _data_cumulative(self):
        probability = []
        for i in range(1, 1000):
            probability.append(i/1000)

        quantiles = stat.genpareto.ppf(probability, self.forma,
                                        loc=self.localizacao,
                                        scale=self.escala)

        dic = {'Vazao': quantiles, 'Probabilidade': probability}

        return pd.DataFrame(dic)
