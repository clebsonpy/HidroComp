from abc import ABCMeta, abstractmethod

import plotly.graph_objs as go
import plotly.express as px
import pandas as pd


class Graphics(metaclass=ABCMeta):

    def __init__(self, obj, color=None, width=None, height=None, size_text=14, xaxis=None,
                 yaxis=None, name=None):
        self.obj = obj
        self.name = name
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

    def __init__(self, data_variable, line=None, color=None, width=None, height=None, size_text=14, xaxis=None,
                 yaxis=None):
        super().__init__(obj=data_variable, color=color, width=width, height=height,
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

    def __init__(self, obj_dhram, color=None, width=None, height=None, size_text=14, xaxis=None, yaxis=None, name=None,
                 data_type=None):
        super().__init__(obj=obj_dhram, color=color, width=width, height=height, size_text=size_text, xaxis=xaxis,
                         yaxis=yaxis, name=name)
        self.data_type = data_type

    def plot(self, type="error_bar"):
        layout = self.layout()

        data = list()
        if type == "point":
            data.append(self._point_simulation())
            fig = dict(data=data, layout=layout)
            return fig, data
        elif type == "box":
            pass
        elif type == "violin":
            pass
        elif type == "error_bar":
            return self._error_bar()
        else:
            raise TypeError


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
    

    def _point_simulation(self):
        point = go.Scatter(x=self.obj.index,
                           y=self.obj[self.obj.index].values,
                           name=self.status.title() + '-impacto',
                           mode='markers',
                           marker=dict(size=8, color=self.color[self.status], line=dict(width=1,
                                                                                        color=self.color[self.status])))

        return point
    """

    def _box(self):
        pass

    def _error_bar(self):
        dic = {"Data": [], "Status": [], "Variable": [], "Error": [], "Error_minus": [], "Text": []}

        for i in self.obj.variables:
            if self.data_type == "mean":
                variable_pre = self.obj.variables[i].sample_pre.mean()
                variable_pos = self.obj.variables[i].sample_pos.mean()
            elif self.data_type == "std":
                variable_pre = self.obj.variables[i].sample_pre.std()
                variable_pos = self.obj.variables[i].sample_pos.std()
            else:
                raise TypeError("Type: mean or std")
            dic["Data"] = dic["Data"] + [variable_pre.mean()]
            dic["Status"] = dic["Status"] + ["Pre-impact"]
            dic["Variable"] = dic["Variable"] + [i]
            dic["Error"] = dic["Error"] + [variable_pre.quantile(self.obj.variables[i].interval[1]) - variable_pre.mean()]
            dic["Error_minus"] = dic["Error_minus"] + [variable_pre.mean() -
                                                       variable_pre.quantile(self.obj.variables[i].interval[0])]
            dic["Text"] = dic["Text"] + [f"{(self.obj.variables[i].interval[1] - self.obj.variables[i].interval[0]) * 100}% "
                                         f"({round(variable_pre.quantile(self.obj.variables[i].interval[0]), 2)}"
                                         f" - {round(variable_pre.quantile(self.obj.variables[i].interval[1]), 2)})"]
            dic["Data"] = dic["Data"] + [variable_pos.mean()]
            dic["Status"] = dic["Status"] + ["Pos-impact"]
            dic["Variable"] = dic["Variable"] + [i]
            dic["Error"] = dic["Error"] + [variable_pos.quantile(self.obj.variables[i].interval[1]) - variable_pos.mean()]
            dic["Error_minus"] = dic["Error_minus"] + [variable_pos.mean() -
                                                       variable_pos.quantile(self.obj.variables[i].interval[0])]
            dic["Text"] = dic["Text"] + [f"{(self.obj.variables[i].interval[1] - self.obj.variables[i].interval[0]) * 100}% "
                                         f"({round(variable_pos.quantile(self.obj.variables[i].interval[0]), 2)}"
                                         f" - {round(variable_pos.quantile(self.obj.variables[i].interval[1]), 2)})"]

        df = pd.DataFrame(dic)
        fig = px.scatter(df, x="Variable", y="Data", color="Status", error_y="Error", error_y_minus="Error_minus",
                         text="Text", labels={"Text": f"Confidence Interval"}, hover_data={"Data": ":.2f"})

        fig.update_traces(mode="markers")
        data = fig["data"]
        fig.layout = self.layout()
        fig.layout.title.text = f"{self.obj.name} - {self.data_type.title()}"
        return fig, data
