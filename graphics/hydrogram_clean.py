import plotly.graph_objs as go

from graphics.hydrogram_biuld import HydrogramBiuld


class HydrogramClean(HydrogramBiuld):

    def __init__(self, data):
        super().__init__()
        self.data = data

    def plot(self, type_criterion=None):
        bandxaxis = go.XAxis(title="Data")
        bandyaxis = go.YAxis(title="Vazão(m³/s)")

        try:
            name = 'Hidrograma - %s' % self.data.name
            layout = dict(title=name,
                          width=1890, height=827,
                          xaxis=bandxaxis, yaxis=bandyaxis,
                          font=dict(family='Time New Roman', size=34,
                                    color='rgb(0,0,0)')
                          )

            data = [self._plot_one(self.data)]
            fig = dict(data=data, layout=layout)
            return data, fig

        except AttributeError:
            name = 'Hidrograma'
            layout = dict(title=name,
                          width=1890, height=827,
                          xaxis=bandxaxis, yaxis=bandyaxis,
                          font=dict(family='Time New Roman', size=34,
                                    color='rgb(0,0,0)')
                          )
            data = self._plot_multi()
            fig = dict(data=data, layout=layout)
            return data, fig

    def _plot_multi(self):
        data = list()
        for i in self.data:
            data.append(self._plot_one(self.data[i]))
        return data
