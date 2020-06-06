import plotly.graph_objs as go


class Boxplot(object):

    def __init__(self, magn_resample=None, datas=None, name=None):
        self.magn_resample = magn_resample
        self.datas = datas
        self.name = name

    def plot(self):
        data = list()
        for i in self.magn_resample:
            data.append((go.Box(y=self.magn_resample[i].values,
                                name='%s Anos' % (i),
                                boxpoints='suspectedoutliers',
                                showlegend=False,
                                marker=dict(
                                    color='rgb(0,0,0)'
                                    )
                                )
                         ))

        layout = dict(title="Magnitudes",
                      showlegend=False,
                      width=1890, height=827,
                      font=dict(family='Time New Roman', size=34, color='rgb(0,0,0)')
                      )

        fig = dict(data=data, layout=layout)
        return fig, data

    def plot_comparasion(self):

        layout = dict(title="Magnitudes",
                      showlegend=False,
                      width=1890, height=827,
                      font=dict(family='Time New Roman', size=34, color='rgb(0,0,0)')
                      )

        fig = dict(data=self.datas, layout=layout)
        return fig, self.datas
