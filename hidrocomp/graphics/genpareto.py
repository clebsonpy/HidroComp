import scipy.stats as stat
import pandas as pd

import plotly.graph_objs as go

from hidrocomp.graphics.distribution_biuld import DistributionBiuld


class GenPareto(DistributionBiuld):

    def __init__(self, title, shape, location, scale):
        super().__init__(title, shape, location, scale)

    def cumulative(self):
        datas = self._data('cumulative')
        data = [go.Scatter(x=datas['peaks'], y=datas['Cumulative'],
                           name=self.title, line=dict(color='rgb(128, 128, 128)',
                                                      width=2))]

        bandxaxis = go.layout.XAxis(title="Vazão(m³/s)")
        bandyaxis = go.layout.YAxis(title="Probabilidade")

        layout = dict(title="GP - Acumulada: %s" % self.title,
                      showlegend=True,
                      width=945, height=827,
                      xaxis=bandxaxis,
                      yaxis=bandyaxis,
                      font=dict(family='Time New Roman', size=28, color='rgb(0,0,0)')
                      )

        fig = dict(data=data, layout=layout)

        return fig, data

    def density(self):
        datas = self._data('density')
        data = [go.Scatter(x=datas['peaks'], y=datas['Density'],
                           name=self.title, line=dict(color='rgb(128, 128, 128)',
                                                      width=2))]

        bandxaxis = go.layout.XAxis(title="Vazão(m³/s)")
        bandyaxis = go.layout.YAxis(title="")

        layout = dict(title="GP - Densidade: %s" % self.title,
                      showlegend=True,
                      width=945, height=827,
                      xaxis=bandxaxis,
                      yaxis=bandyaxis,
                      font=dict(family='Time New Roman', size=28, color='rgb(0,0,0)')
                      )

        fig = dict(data=data, layout=layout)
        return fig, data

    def _data_density(self):

        cumulative = self._data_cumulative()
        density = stat.genpareto.pdf(cumulative['peaks'].values, self.shape,
                                     loc=self.location, scale=self.scale)

        dic = {'peaks': cumulative['peaks'].values, 'Density': density}

        return pd.DataFrame(dic)

    def _data_cumulative(self):
        probability = list()
        for i in range(1, 1000):
            probability.append(i/1000)

        quantiles = stat.genpareto.ppf(probability, self.shape,
                                       loc=self.location,
                                       scale=self.scale)

        dic = {'peaks': quantiles, 'Cumulative': probability}

        return pd.DataFrame(dic)
