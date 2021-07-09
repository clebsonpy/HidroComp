import plotly.graph_objs as go
from hidrocomp.graphics.hydrogram_build import HydrogramBuild


class HydrogramParcial(HydrogramBuild):

    def __init__(self, data, peaks, threshold, threshold_criterion=None, type_criterion=None, width=None,
                 height=None, size_text=None, title=None, station=None, color=None, line_threshold: bool = True,
                 point_start_end: bool = True):
        super().__init__(width=width, height=height, size_text=size_text, title=title)
        self.color = color
        self.peaks = peaks
        self.station = station
        self.data = data[self.station].to_frame()
        self.threshold = threshold
        self.type_criterion = type_criterion
        self.threshold_criterion = threshold_criterion
        self.line_threshold = line_threshold
        self.point_start_end = point_start_end

    def plot(self):
        bandxaxis = go.layout.XAxis(title="Date")
        bandyaxis = go.layout.YAxis(title="Flow(m³/s)")

        try:
            if self.threshold_criterion is None:
                raise AttributeError

            layout = self.layout(bandxaxis=bandxaxis, bandyaxis=bandyaxis)

            data = []

            for i in self.data:
                try:
                    color = self.color[i]
                except:
                    color = None
            data.append(self._plot_one(self.data, station=self.station, color=color))
            data.append(self._plot_threshold())
            if self.type_criterion is not None:
                data.append(self._plot_threshold_criterion())

            if len(self.peaks) > 0:
                data += self._plot_event_peaks()

            fig = dict(data=data, layout=layout)
            return fig, data

        except AttributeError:

            layout = self.layout(bandxaxis=bandxaxis, bandyaxis=bandyaxis)

            data = []
            for i in self.data:
                try:
                    color = self.color[i]
                except:
                    color = None

            data.append(self._plot_one(self.data, station=self.station, color=color))
            if self.line_threshold:
                data.append(self._plot_threshold())

            if len(self.peaks) > 0:
                data += self._plot_event_peaks()

            fig = dict(data=data, layout=layout)
            return fig, data

    def _plot_event_peaks(self):
        points = []
        if self.point_start_end:
            point_start = go.Scatter(
                x=list(self.peaks.Start),
                y=self.data.loc[self.peaks.Start].T.values[0],
                name="Start of events",
                mode='markers',
                marker=dict(color='rgb(0, 0, 0)',
                            symbol='circle-dot',
                            size=6),
                opacity=1)
            points.append(point_start)
            point_end = go.Scatter(
                x=list(self.peaks.End),
                y=self.data.loc[self.peaks.End].T.values[0],
                name="Ends of events",
                mode='markers',
                marker=dict(color='rgb(0, 0, 0)',
                            size=6,
                            symbol="x-dot"),
                opacity=1)
            points.append(point_end)
        point_vazao = go.Scatter(
            x=self.peaks['Peaks'].index,
            y=self.peaks['Peaks'].values,
            name="Peaks",
            mode='markers',
            marker=dict(size=8,
                        color='rgb(128, 128, 128)',
                        line=dict(width=1,
                                  color='rgb(0, 0, 0)'),),
            opacity=1)
        points.append(point_vazao)
        return points

    def _plot_threshold(self):
        trace_threshold = go.Scatter(
            x=self.data.index,
            y=[self.threshold]*len(self.data),
            name="Threshold",
            line=dict(color='rgb(128, 128, 128)',
                      width=1.5,
                      dash='dot')
        )

        return trace_threshold

    def _plot_threshold_criterion(self):
        trace_threshold_criterion = go.Scatter(
            x=self.data.index,
            y=[self.threshold_criterion]*len(self.data),
            name=self.type_criterion,
            line=dict(color='rgb(128, 128, 128)',
                      width=1.5,
                      dash='dash')
        )
        return trace_threshold_criterion
