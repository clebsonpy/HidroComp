import plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF
import colorlover as cl
import cufflinks as cf

from graphics.hydrogram_biuld import HydrogramBiuld


class HydrogramParcial(HydrogramBiuld):

    def __init__(self, data, peaks, threshold, threshold_criterion=None):
        super().__init__()
        self.data = data
        self.peaks = peaks
        self.threshold = threshold
        self.threshold_criterion = threshold_criterion

    def plot(self, type_criterion):
        bandxaxis = go.XAxis(
            title="Data",
        )

        bandyaxis = go.YAxis(
            title="Vazão(m³/s)",
        )

        try:
            if self.threshold_criterion is None:
                raise AttributeError
            name = 'Hidrograma Parcial - %s' % self.data.name
            layout = dict(
                title=name.title(),
                xaxis=bandxaxis,
                yaxis=bandyaxis,
                font=dict(family='Courier New, monospace', size=16, color='#7f7f7f'))

            data = []
            data.append(self._plot_one(self.data))
            data.append(self._plot_threshold())
            data.append(self._plot_threshold_criterion(type_criterion))
            data += self._plot_event_peaks()

            fig = dict(data=data, layout=layout)
            py.offline.plot(fig, filename='gráficos/'+ name.replace(' - ', '_') +'.html')
        except AttributeError:
            name = 'Hidrograma Parcial - %s' % self.data.name
            layout = dict(
                title=name,
                xaxis=bandxaxis,
                yaxis=bandyaxis,
                font=dict(family='Courier New, monospace', size=16, color='#7f7f7f'))

            data = []
            data.append(self._plot_one(self.data))
            data.append(self._plot_threshold())
            data += self._plot_event_peaks()

            fig = dict(data=data, layout=layout)
            py.offline.plot(fig, filename='gráficos/'+ name.replace(' - ', '_') +'.html')

    def _plot_event_peaks(self):
        point_start = go.Scatter(x=self.peaks.Inicio,
                y=self.data.loc[self.peaks.Inicio],
                name = "Inicio do Evento",
                mode='markers',
                marker=dict(color='blue',
                             size = 5),
                opacity = 0.75)
        point_end = go.Scatter(x=self.peaks.Fim,
            y=self.data.loc[self.peaks.Fim],
            name = "Fim do Evento",
            mode='markers',
            marker=dict(color='red',
                         size = 5),
            opacity = 0.75)
        point_vazao = go.Scatter(x=self.peaks.index,
            y=self.data.loc[self.peaks.index],
            name = "Pico",
            mode='markers',
            marker=dict(color='green',
                         size = 5),
            opacity = 1)

        return [point_start, point_end, point_vazao]

    def _plot_threshold(self):
        trace_threshold = go.Scatter(x=self.data.index,
            y=[self.threshold]*len(self.data),
            name = "Limiar",
            line = dict(color = 'rgb(0, 230, 0)', width = 0.75))
        return trace_threshold

    def _plot_threshold_criterion(self, type_criterion):
        trace_threshold_criterion = go.Scatter(x=self.data.index,
                y=[self.threshold_criterion]*len(self.data),
                name = type_criterion.title(),
                line = dict(color = 'rgb(255, 64, 0)', width = 0.75))
        return trace_threshold_criterion
