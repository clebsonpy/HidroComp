import plotly.graph_objs as go
import pandas as pd

from hidrocomp.graphics.hydrogram_build import HydrogramBuild


class HydrogramAnnual(HydrogramBuild):

    def __init__(self, data, peaks, data_type: str, width: int = None, height: int = None, size_text: int = None,
                 title=None, station=None, showlegend: bool = True, language: str = 'pt'):
        self.data = pd.DataFrame(data)
        self.peaks = peaks
        self.station = station
        self.language = language
        self.data_type = data_type
        super().__init__(width=width, height=height, size_text=size_text, title=title, showlegend=showlegend)

    def plot(self):
        bandxaxis = go.layout.XAxis(title=self.x_axis_title[self.language])
        bandyaxis = go.layout.YAxis(title=self.y_axis_title[self.data_type][self.language])

        layout = self.layout(bandxaxis=bandxaxis, bandyaxis=bandyaxis)

        data = list()
        data.append(self._plot_one(data=self.data, station=self.station, color='rgb(0,0,0)'))
        data.append(self._plot_event_peaks())

        fig = dict(data=data, layout=layout)
        return fig, data

    def _plot_event_peaks(self):
        peaks_name = {'pt': 'Picos', 'en': 'Peaks'}
        point_peak = go.Scatter(x=self.peaks['Peaks'].index,
                                y=self.peaks['Peaks'].values,
                                name=peaks_name[self.language],
                                mode='markers',
                                marker=dict(size=8, color='rgb(128, 128, 128)', line=dict(width=1, color='rgb(0, 0, 0)')
                                            ),
                                opacity=1)

        return point_peak
