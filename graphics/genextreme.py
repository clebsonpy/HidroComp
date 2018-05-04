import scipy.stats as stat
import pandas as pd

import plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF
import colorlover as cl
import cufflinks as cf

from graphics.distribution_biuld import DistributionBiuld


class GenExtreme(DistributionBiuld):

    def __init__(self, title, forma, localizacao, escala):
        super().__init__(title, forma, localizacao, escala)

    def cumulative(self):
        dados = self._data('cumulative')
        data = go.Scatter(x=dados['Vazao'], y=dados['Probabilidade'],
                              name=self.title,
                              line = dict(color = 'rgb(128, 128, 128)',
                                          width = 1.5))
        data_figs = [data]

        bandxaxis = go.XAxis(title="Vazão(m³/s)")
        bandyaxis = go.YAxis(title="Probabilidade")

        layout = dict(title="GEV - Acumulada: %s" % self.title,
                      showlegend=True,
                      width=945, height=827,
                      xaxis=bandxaxis,
                      yaxis=bandyaxis,
                      font=dict(family='Time New Roman', size=34, color='rgb(0,0,0)'))

        fig = dict(data=data_figs, layout=layout)
        name_graphic = 'GEV_Acumulada_%s' % self.title
        py.offline.plot(fig, filename='gráficos/'+ name_graphic +'.html')

        return data, fig

    def density(self):
        dados = self._data('density')
        data = go.Scatter(x=dados['Vazao'], y=dados['Densidade'],
                          name=self.title,
                          line = dict(color = 'rgb(128, 128, 128)',
                                      width = 1.5))
        data_fig = [data]

        bandxaxis = go.XAxis(title="Vazão(m³/s)")
        bandyaxis = go.YAxis(title="")

        layout = dict(title="GEV - Densidade: %s" % self.title,
                      showlegend=True,
                      width=945, height=827,
                      xaxis=bandxaxis,
                      yaxis=bandyaxis,
                      font=dict(family='Time New Roman', size=34, color='rgb(0,0,0)'))

        fig = dict(data=data_fig, layout=layout)
        name_graphic = 'GEV_Densidade_%s' % self.title
        py.offline.plot(fig, filename='gráficos/'+ name_graphic + '.html')

        return data, fig

    def _data_density(self):

        cumulative = self._data_cumulative()
        density = stat.genextreme.pdf(cumulative['Vazao'].values, self.forma,
                                 loc=self.localizacao, scale=self.escala)

        dic = {'Vazao': cumulative['Vazao'].values, 'Densidade': density}

        return pd.DataFrame(dic)

    def _data_cumulative(self):
        probability = []
        for i in range(1, 1000):
            probability.append(i/1000)

        quantiles = stat.genextreme.ppf(probability, self.forma,
                                        loc=self.localizacao,
                                        scale=self.escala)

        dic = {'Vazao': quantiles, 'Probabilidade': probability}

        return pd.DataFrame(dic)
