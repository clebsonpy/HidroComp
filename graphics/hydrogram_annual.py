import plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF
import colorlover as cl
import cufflinks as cf

from graphics.hydrogram_biuld import HydrogramBiuld


class HydrogramAnnual(HydrogramBiuld):

    def __init__(self, data, peaks):
        super().__init__()
        self.data = data
        self.peaks = peaks

    def plot(self):
        bandxaxis = go.XAxis(
            title="Data",
        )

        bandyaxis = go.YAxis(
            title="Vazão(m³/s)",
        )

        name = 'Hidrograma Máximas Anuais'
        layout = dict(
            title = "Hidrograma Série Máximas Anuais",
            width=1890, height=827,
            xaxis=bandxaxis,
            yaxis=bandyaxis,
            font=dict(family='Time New Roman', size=34, color='rgb(0,0,0)'))

        data = []
        data.append(self._plot_one(self.data))
        data.append(self._plot_event_peaks())

        fig = dict(data=data, layout=layout)
        py.offline.plot(fig, filename='gráficos/'+ name.replace(' - ', '_') +'.html')

    def _plot_event_peaks(self):
        point_vazao = go.Scatter(x=self.peaks.index,
            y=self.data.loc[self.peaks.index],
            name = "Pico",
            mode='markers',
            marker=dict(color='green',
                         size = 5),
            opacity = 1)

        return point_vazao
