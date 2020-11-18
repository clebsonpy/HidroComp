import plotly.graph_objs as go
import pandas as pd

from hidrocomp.graphics.hydrogram_build import HydrogramBuild


class HydrogramAnnual(HydrogramBuild):

    def __init__(self, data, peaks, width=None, height=None, size_text=None, title=None, station=None):
        self.data = pd.DataFrame(data)
        self.peaks = peaks
        self.station = station
        super().__init__(width=width, height=height, size_text=size_text, title=title)

    def plot(self):
        bandxaxis = go.layout.XAxis(title="Data")
        bandyaxis = go.layout.YAxis(title="Vazão(m³/s)")

        layout = dict(
            title=dict(text=self.title, x=0.5, xanchor='center', y=0.95, yanchor='top',
                       font=dict(family='Courier New, monospace', size=self.size_text + 10)),
            xaxis=bandxaxis,
            yaxis=bandyaxis,
            width=self.width, height=self.height,
            font=dict(family='Courier New, monospace', size=self.size_text, color='#7f7f7f'),
            showlegend=True, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')

        data = list()
        data.append(self._plot_one(data=self.data, station=self.station, color='rgb(0,0,0)'))
        data.append(self._plot_event_peaks())

        fig = dict(data=data, layout=layout)
        return fig, data

    def _plot_event_peaks(self):
        point_peak = go.Scatter(x=self.peaks['Peaks'].index,
                                y=self.peaks['Peaks'].values,
                                name="Pico",
                                mode='markers',
                                marker=dict(size=8, color='rgb(128, 128, 128)', line=dict(width=1, color='rgb(0, 0, 0)')
                                            ),
                                opacity=1)

        return point_peak
