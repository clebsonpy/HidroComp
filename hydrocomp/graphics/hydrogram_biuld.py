import plotly.graph_objs as go

from abc import ABCMeta, abstractmethod


class HydrogramBiuld(object, metaclass=ABCMeta):

    @abstractmethod
    def plot(self, type_criterion=None):
        pass

    def _plot_one(self, data):
        
        data = go.Scatter(x=data[data.columns.values[0]].index,
                          y=data[data.columns.values[0]].values,
                          name=data[data.columns.values[0]].name,
                          line=dict(width=1, color='rgb(0,0,0)'),
                          opacity=1, connectgaps=False, )

        return data
