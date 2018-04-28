import scipy.stats as stat

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
        dados = self._data()
        data_fig = go.Scatter(x=dados[self.title], y=dados.index,
                              name=self.title.title())
        data_figs = [data_fig]

        bandxaxis = go.XAxis(title="Vazão(m³/s)")
        bandyaxis = go.YAxis(title="Probabilidade")

        layout = dict(title="GEV - Acumulada", xaxis=bandxaxis, width=840, height=672,
                      yaxis=bandyaxis,
                      font=dict(family='Courier New, monospace', size=12,
                                color='#7f7f7f'))

        fig = dict(data=data_figs, layout=layout)
        name_graphic = 'GEV_Acumulada_%s' % self.title
        py.offline.plot(fig, filename='gráficos/'+ name_graphic +'.html')

        def density(self):
            pass
