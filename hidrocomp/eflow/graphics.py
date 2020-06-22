from abc import ABCMeta, abstractmethod

import plotly.graph_objs as go
import pandas as pd


class Graphics(metaclass=ABCMeta):

    def __init__(self, data_variable, status, color=None, width=None, height=None, size_text=14, xaxis=None,
                 yaxis=None, name=None):
        self.data = data_variable.sort_index()
        self.name = name
        self.status = status
        self.width = width
        self.height = height
        self.size_text = size_text
        self.color = color
        self.xaxis = xaxis
        self.yaxis = yaxis

    @abstractmethod
    def plot(self):
        pass

    def layout(self):
        bandxaxis = go.layout.XAxis(title=self.xaxis)
        bandyaxis = go.layout.YAxis(title=self.yaxis)
        layout = dict(
            title=dict(text=self.name, x=0.5, xanchor='center', y=0.95, yanchor='top',
                       font=dict(family='Courier New, monospace', size=self.size_text + 10)),
            xaxis=bandxaxis,
            yaxis=bandyaxis,
            width=self.width, height=self.height,
            font=dict(family='Courier New, monospace', size=self.size_text, color='rgb(0,0,0)'),
            showlegend=True, plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF')

        return layout


class GraphicsRVA(Graphics):

    def __init__(self, data_variable, status, line=None, color=None, width=None, height=None, size_text=14, xaxis=None,
                 yaxis=None):
        super().__init__(data_variable=data_variable, status=status, color=color, width=width, height=height,
                         size_text=size_text, xaxis=xaxis, yaxis=yaxis)
        self.line = line

    def _plot_rva(self, line):
        dash = {"upper_line": "dot", "lower_line": "dash"}
        line_graph = go.Scatter(x=self.data.index,
                                y=[self.line[line][self.name]] * len(self.data.index),
                                name=line.title(),
                                mode='lines',
                                line=dict(width=1, dash=dash[line], color='rgb(0, 0, 0)'),
                                opacity=1, connectgaps=False)
        return line_graph

    def _plot_iha(self):
        point = go.Scatter(x=self.data.index,
                           y=self.data.loc[self.data.index].values,
                           name=self.status.title()+'-impacto',
                           mode='markers+lines',
                           marker=dict(size=8, color=self.color[self.status], line=dict(width=1,
                                                                                        color=self.color[self.status])))

        return point

    def plot(self):
        layout = self.layout()

        data = list()
        data.append(self._plot_iha())
        try:
            for i in self.line:
                if i != 'median_line':
                    data.append(self._plot_rva(i))
        except:
            pass

        fig = dict(data=data, layout=layout)
        return fig, data


class GraphicsDHRAM(Graphics):

    def __init__(self, data_variable, status, color=None, width=None, height=None, size_text=14, xaxis=None,
                 yaxis=None, name=None):
        super().__init__(data_variable=data_variable, status=status, color=color, width=width, height=height,
                         size_text=size_text, xaxis=xaxis, yaxis=yaxis, name=name)

    def plot(self, type="violin"):
        layout = self.layout()

        data = list()
        if type == "point":
            data.append(self._point_simulation())
        elif type == "box":
            pass
        elif type == "violin":
            pass
        else:
            raise TypeError
        fig = dict(data=data, layout=layout)
        return fig, data

    """"
    def _line_interval_confidence(self):
        x = list(self.data.index.values)
        x_rev = x[::-1]
        y_lower = [self.interval_confidence.values[0]] * len(self.data.index)
        y_upper = [self.interval_confidence.values[1]] * len(self.data.index)
        y_lower = y_lower[::-1]

        trace = go.Scatter(
            x=x+x_rev, y=y_upper+y_lower,
            fill='toself')

        return trace
    """

    def _point_simulation(self):
        point = go.Scatter(x=self.data.index,
                           y=self.data[self.data.index].values,
                           name=self.status.title() + '-impacto',
                           mode='markers',
                           marker=dict(size=8, color=self.color[self.status], line=dict(width=1,
                                                                                        color=self.color[self.status])))

        return point


    def _box(self):
        pass

    def _violin(self):
        pass
