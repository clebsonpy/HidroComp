import scipy.stats as stat

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

        layout = dict(title="GP - Acumulada", xaxis=bandxaxis, width=840, height=672,
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

        layout = dict(title="GP - Densidade", xaxis=bandxaxis, width=840,
                      height=672, yaxis=bandyaxis,
                      font=dict(family='Courier New, monospace', size=16,
                                color='#7f7f7f'))

        fig = dict(data=data_fig, layout=layout)
        name_graphic = 'GP_Densidade_%s' % self.title
        py.offline.plot(fig, filename='gráficos/'+ name_graphic + '.html')

        return data
