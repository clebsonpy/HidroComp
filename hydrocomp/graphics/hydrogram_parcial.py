import plotly.graph_objs as go

from hydrocomp.graphics.hydrogram_biuld import HydrogramBiuld


class HydrogramParcial(HydrogramBiuld):

    def __init__(self, data, peaks, threshold, title, threshold_criterion=None):
        super().__init__()
        self.data = data
        self.peaks = peaks
        self.threshold = threshold
        self.threshold_criterion = threshold_criterion
        self.title = title

    def plot(self, type_criterion=None, width=None, height=None, size_text=None):
        bandxaxis = go.layout.XAxis(title="Data")
        bandyaxis = go.layout.YAxis(title="Vazão(m³/s)")

        try:
            if self.threshold_criterion is None:
                raise AttributeError

            name = 'Hidrograma Série de Duração Parcial - %s' % self.title
            layout = dict(
                title=name,
                showlegend=True,
                width=width, height=height,
                xaxis=bandxaxis, yaxis=bandyaxis,
                font=dict(family='Time New Roman', size=size_text, color='rgb(0,0,0)'))

            data = []
            data.append(self._plot_one(self.data))
            data.append(self._plot_threshold())
            if type_criterion is not None:
                data.append(self._plot_threshold_criterion(type_criterion))
            data += self._plot_event_peaks()

            fig = dict(data=data, layout=layout)
            return fig, data

        except AttributeError:
            name = 'Hidrograma Série de Duração Parcial -  %s' % self.title
            layout = dict(
                title=name,
                showlegend=True,
                width=width, height=height,
                xaxis=bandxaxis, yaxis=bandyaxis,
                font=dict(family='Time New Roman', size=size_text, color='rgb(0,0,0)'))

            data = []
            data.append(self._plot_one(self.data))
            data.append(self._plot_threshold())
            data += self._plot_event_peaks()

            fig = dict(data=data, layout=layout)
            return fig, data


    def _plot_event_peaks(self):
        point_start = go.Scatter(
            x=list(self.peaks.Start),
            y=self.data[self.data.columns.values[0]].loc[self.peaks.Start].values,
            name="Inicio do Evento",
            mode='markers',
            marker=dict(color='rgb(0, 0, 0)',
                        symbol='circle-dot',
                        size=6),
            opacity=1)

        point_end = go.Scatter(
            x=list(self.peaks.End),
            y=self.data[self.data.columns.values[0]].loc[self.peaks.End].values,
            name="Fim do Evento",
            mode='markers',
            marker=dict(color='rgb(0, 0, 0)',
                        size=6,
                        symbol="x-dot"),
            opacity=1)

        point_vazao = go.Scatter(
            x=self.peaks.index,
            y=self.peaks.peaks.values,
            name="Pico",
            mode='markers',
            marker=dict(size=8,
                        color='rgb(128, 128, 128)',
                        line=dict(width=1,
                                  color='rgb(0, 0, 0)'),),
            opacity=1)

        return [point_start, point_end, point_vazao]

    def _plot_threshold(self):
        trace_threshold = go.Scatter(
            x=self.data.index,
            y=[self.threshold]*len(self.data),
            name="Limiar",
            line=dict(color='rgb(128, 128, 128)',
                      width=1.5,
                      dash='dot')
        )

        return trace_threshold

    def _plot_threshold_criterion(self, type_criterion):
        trace_threshold_criterion = go.Scatter(
            x=self.data.index,
            y=[self.threshold_criterion]*len(self.data),
            name="Criterion",
            line=dict(color='rgb(128, 128, 128)',
                      width=1.5,
                      dash='dash')
        )
        return trace_threshold_criterion
