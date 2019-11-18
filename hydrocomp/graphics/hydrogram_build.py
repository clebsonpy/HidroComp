import plotly.graph_objs as go

from abc import ABCMeta, abstractmethod


class HydrogramBuild(metaclass=ABCMeta):

    def __init__(self, width=None, height=None, title=None, size_text=None):
        self.width = width
        self.height = height
        self.title = title
        self.size_text = size_text

    @abstractmethod
    def plot(self):
        pass

    def _plot_one(self, data, name, color=None):
        data = go.Scatter(x=data.index,
                          y=data.T.values[0],
                          name=name,
                          line=dict(width=1, color=color),
                          opacity=1, connectgaps=False)
        return data
