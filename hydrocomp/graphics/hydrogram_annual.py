import plotly.graph_objs as go
import pandas as pd

from hydrocomp.graphics.hydrogram_build import HydrogramBuild


class HydrogramAnnual(HydrogramBuild):

    def __init__(self, data, peaks, width=None, height=None, size_text=None, title=None):
        self.data = data
        self.peaks = peaks
        super().__init__(width=width, height=height, size_text=size_text, title=title)

    def plot(self):
        bandxaxis = go.layout.XAxis(title="Data")
        bandyaxis = go.layout.YAxis(title="Vazão(m³/s)")

        layout = dict(title=self.title,
                      width=self.width, height=self.height,
                      xaxis=bandxaxis, yaxis=bandyaxis,
                      font=dict(family='Time New Roman', size=self.size_text, color='rgb(0,0,0)')
                      )

        data = list()
        data.append(self._plot_one(data=self.data, name='Pico', color='rgb(0,0,0)'))
        data.append(self._plot_event_peaks())

        fig = dict(data=data, layout=layout)
        return fig, data

    def _plot_event_peaks(self):
        point_peak = go.Scatter(x=self.peaks['peaks'].index,
                                y=self.peaks['peaks'].values,
                                name="Pico",
                                mode='markers',
                                marker=dict(size=8, color='rgb(128, 128, 128)', line=dict(width=1, color='rgb(0, 0, 0)')
                                            ),
                                opacity=1)

        return point_peak
