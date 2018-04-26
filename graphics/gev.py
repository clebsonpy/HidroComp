import scipy.stats as stat

import plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF
import colorlover as cl
import cufflinks as cf

from graphics.distribution_biuld import DistributionBiuld


class Gev(DistributionBiuld):

    def __init__(self, title, forma, localizacao, escala):
        super().__init__(title, forma, localizacao, escala)

    def cumulative(self):
        data = []
        for i in self._data():
            line = go.Scatter(x=dados[i], y=dados.index, name=i)
            data.append(line)

        bandxaxis = go.XAxis(title="Vazão(m³/s)")

        bandyaxis = go.YAxis(title="Probabilidade")

        layout = dict(title="Generalizada de Pareto", xaxis=bandxaxis,
                    yaxis=bandyaxis,
                    dth=840,
                    height=672,
                    font=dict(family='Courier New, monospace', size=12,
                            color='#7f7f7f'))

        fig = dict(data=data, layout=layout)
        py.offline.plot(fig, filename='gráficos/GEV_Acumulada' + '.html')

        def density(self):
            pass
