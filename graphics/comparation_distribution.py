import plotly as plot
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF
import colorlover as cl
import cufflinks as cf


class Comparation_Distribution(object):

    def __init__(self, figs):
        self.figs = figs

    def plot(self):
        bandxaxis = go.XAxis(title="Vazão(m³/s)")
        bandyaxis = go.YAxis(title="")

        layout = dict(title="Generalizada de Pareto",
                      showlegend=True,
                      width=945, height=827,
                      xaxis=bandxaxis,
                      yaxis=bandyaxis,
                      font=dict(family='Time New Roman', size=34, color='rgb(0,0,0)'))

        fig = dict(data=self.figs, layout=layout)
        name_graphic = 'GP_Densidade_'
        plot.offline.plot(fig, filename='gráficos/' + name_graphic + '.html')
        py.image.save_as(fig, filename='gráficos/'+name_graphic+'.png')
        return fig
