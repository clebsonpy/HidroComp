import plotly.graph_objs as go

from abc import ABCMeta, abstractmethod


class HydrogramBiuld(metaclass=ABCMeta):

    def __init__(self, width=None, height=None, title=None, size_text=None):
        self.width = width
        self.height = height
        self.title = title
        self.size_text = size_text

    @abstractmethod
    def plot(self):
        pass

    def _plot_one(self, data):

        data = go.Scatter(x=data[data.columns.values[0]].index,
                          y=data[data.columns.values[0]].values,
                          name=data[data.columns.values[0]].name,
                          line=dict(width=1, color='rgb(0,0,0)'),
                          opacity=1, connectgaps=False)
        return data
