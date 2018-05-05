import pandas as pd
import plotly as py
import plotly.plotly as save
import plotly.graph_objs as go

class Boxplot(object):

    def __init__(self, magn_resample=None, figs=None, name=None):
        self.magn_resample = magn_resample
        self.figs = figs
        self.name = name

    def plot(self):
        data = []
        for i in self.magn_resample:
            data.append((go.Box(y=self.magn_resample[i].values,
                                name = '%s Anos' % (i),
                                boxpoints='suspectedoutliers',
                                showlegend = False,
                                #jitter=0.3,
                                #pointpos=-1.8,
                                marker=dict(
                                    color='rgb(0,0,0)'
                                    )
                                )
                        ))


        layout = dict(title="Magnitudes",
                      showlegend=False,
                      width=1890, height=827,
                      font=dict(family='Time New Roman', size=34, color='rgb(0,0,0)'))

        fig = dict(data=data, layout=layout)
        py.offline.plot(fig, filename='gráficos/boxplot.html')
        return data, fig

    def plot_comparasion(self):

        layout = dict(title="Magnitudes",
                      showlegend=False,
                      width=1890, height=827,
                      font=dict(family='Time New Roman', size=34, color='rgb(0,0,0)'))

        fig = dict(data=self.figs, layout=layout)
        py.offline.plot(fig, filename='gráficos/boxplot.html')
        #save.image.save_as(fig, filename='gráficos/boxplot_group.png')
