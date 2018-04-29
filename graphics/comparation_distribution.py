import plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF
import colorlover as cl
import cufflinks as cf


class Comparation_Distribution(object):

    def __init__(self, figs, para):
        self.figs = figs

    def plot(self):
        bandxaxis = go.XAxis(title="Vazão(m³/s)")
        bandyaxis = go.YAxis(title="Probabilidade")

        layout = dict(title="Generalizada de Pareto", xaxis=bandxaxis, width=840, height=672,
                      yaxis=bandyaxis,
                      font=dict(family='Courier New, monospace', size=16,
                                color='#7f7f7f'))

        fig = dict(data=self.figs, layout=layout)
        name_graphic = 'GP_Acumulada'
        py.offline.plot(fig, filename='gráficos/' + name_graphic + '.html')

        return fig

    def rmae(self):
        pass

    def rmse(self):
        pass

    def mae(self):
        pass
