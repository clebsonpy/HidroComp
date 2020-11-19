import plotly.graph_objs as go

from abc import ABCMeta, abstractmethod


class HydrogramBuild(metaclass=ABCMeta):

    colobar_title = {'pt': 'Ano', 'en': 'Year'}
    threshold_title = {'pt': 'Limiar', 'en': 'Threshold'}
    x_axis_title = {'pt': 'Data', 'en': 'Date'}
    y_axis_title = {'pt': 'Vazão (m³/s)', 'en': 'Flow (m³/s)'}

    def __init__(self, width=None, height=None, title=None, size_text=None, showlegend=None):
        self.width = width
        self.height = height
        self.title = title
        self.size_text = size_text
        self.showlegend = showlegend

    def layout(self, bandxaxis, bandyaxis):
        layout = dict(
            title=dict(text=self.title, x=0.5, xanchor='center', y=0.95, yanchor='top',
                       font=dict(family='Courier New, monospace', size=self.size_text + 10)),
            xaxis=bandxaxis,
            yaxis=bandyaxis,
            width=self.width, height=self.height,
            font=dict(family='Courier New, monospace', size=self.size_text, color='rgb(0,0,0)'),
            showlegend=self.showlegend, plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF')

        return layout

    @abstractmethod
    def plot(self):
        pass

    def _plot_one(self, data, station=None, color=None):
        data = go.Scatter(x=data.index,
                          y=data.T.values[0],
                          name=station,
                          line=dict(width=1, color=color),
                          opacity=1, connectgaps=False)
        return data
