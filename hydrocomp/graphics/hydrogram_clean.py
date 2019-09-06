import plotly.graph_objs as go

from hydrocomp.graphics.hydrogram_biuld import HydrogramBiuld


class HydrogramClean(HydrogramBiuld):

    def __init__(self, data):
        super().__init__()
        self.data = data

    def plot(self, type_criterion=None, width=None, height=None, size_text=None):
        bandxaxis = go.layout.XAxis(title="Data")
        bandyaxis = go.layout.YAxis(title="Vazão(m³/s)")

        try:
            layout = dict(title="Hidrograma",
                          width=width, height=height,
                          xaxis=bandxaxis, yaxis=bandyaxis,
                          font=dict(family='Time New Roman', size=size_text, color='rgb(0,0,0)')
                          )

            data = list()
            data.append(self._plot_one(self.data))
            fig = dict(data=data, layout=layout)
            return fig, data

        except AttributeError:
            name = 'Hidrograma'
            layout = dict(title=name,
                          width=width, height=height,
                          xaxis=bandxaxis, yaxis=bandyaxis,
                          font=dict(family='Time New Roman', size=size_text))

            data = list()
            data.append(self._plot_multi())
            fig = dict(data=data, layout=layout)
            return fig, data

    def _plot_multi(self):
        data = list()
        for i in self.data:
            data += self._plot_one(self.data[i])
        return data
