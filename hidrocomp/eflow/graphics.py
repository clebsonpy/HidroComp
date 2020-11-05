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
                 yaxis=None, status=None):
        super().__init__(obj=data_variable, color=color, width=width, height=height,
                         size_text=size_text, xaxis=xaxis, yaxis=yaxis)
        self.line = line
        self.status = status

    def _plot_rva(self, line):
        print(self.obj.name)
        dash = {"upper_line": "dot", "lower_line": "dash"}
        line_graph = go.Scatter(x=self.obj.data.index,
                                y=[self.line[line][self.obj.name]] * len(self.obj.data.index),
                                name=line.title(),
                                mode='lines',
                                line=dict(width=1, dash=dash[line], color='rgb(0, 0, 0)'),
                                opacity=1, connectgaps=False)
        return line_graph

    def _plot_iha(self):
        point = go.Scatter(x=self.obj.data.index,
                           y=self.obj.data.loc[self.obj.data.index].values,
                           name=self.status.title()+'-impacto',
                           mode='markers+lines',
                           marker=dict(size=8, color=self.color[self.status], line=dict(width=1,
                                                                                        color=self.color[self.status])))

        return point

    def plot(self):
        layout = self.layout()

        data = list()
        data.append(self._plot_iha())

        for i in self.line:
            if i != 'median_line':
                data.append(self._plot_rva(i))



        fig = dict(data=data, layout=layout)
        return fig, data


class GraphicsCha(Graphics):

    def __init__(self, obj_dhram, color=None, width=None, height=None, size_text=14, xaxis=None, yaxis=None, name=None,
                 data_type=None, names_variables: dict = None):
        super().__init__(obj=obj_dhram, color=color, width=width, height=height, size_text=size_text, xaxis=xaxis,
                         yaxis=yaxis, name=name)
        self.data_type = data_type
        self.names_variables = names_variables

    def plot(self, type="error_bar", by_type_events=None):
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
            return self._error_bar(by_type_events)
        else:
            raise TypeError

    def _box(self):
        pass

    def _error_bar(self, by_type_events):
        dic = {"Data": [], "Status": [], "Variable": [], "Error": [], "Error_minus": [], "Text": []}
        events_high = ["1-day maximum", "Date of maximum", "High events count", "High events duration"]
        events_low = ["1-day minimum", "Date of minimum", "Low events count", "Low events duration"]

        # names = {"1-day maximum": "1-day", "Date of maximum": "Date", "High events count": "Count",
        #          "High events duration": "Duration", "1-day minimum": "1-day", "Date of minimum": "Date",
        #          "Low events count": "Count", "Low events duration": "Duration"}

        dict_events = {"High": events_high, "Low": events_low}
        if self.data_type == "mean":
            if self.obj.name in dict_events[by_type_events]:
                variable_diff = self.obj.value_mean
                variable = {"Diff": variable_diff}
            else:
                return None
        elif self.data_type == "std":
            if self.obj.name in dict_events[by_type_events]:
                variable_diff = self.obj.value_std
                variable = {"Diff": variable_diff}
            else:
                return None
        else:
            if self.obj.name in dict_events[by_type_events]:
                variable_diff_mean = self.obj.value_mean
                variable_diff_std = self.obj.value_std
                variable = {"Mean": variable_diff_mean, "Std": variable_diff_std}
            else:
                return None

        for j in variable:
            dic["Data"] = dic["Data"] + [variable[j]["Pos - mean"].values[0]]
            dic["Status"] = dic["Status"] + [j]
            dic["Variable"] = dic["Variable"] + [self.names_variables[self.obj.name] + "("+j+")"
                                                 if self.obj.name in self.names_variables.keys() else self.obj.name]
            dic["Error"] = dic["Error"] + [variable[j]["Pos - 97_5"].values[0] - variable[j]["Pos - mean"].values[0]]
            dic["Error_minus"] = dic["Error_minus"] + [variable[j]["Pos - mean"].values[0] - variable[j]["Pos - 2_5"].values[0]]

            dic["Text"] = dic["Text"] + [f"{(self.obj.interval[1] - self.obj.interval[0]) * 100}% "
                                         f"({round(variable[j]['Pos - 2_5'].values[0], 2)}"
                                         f"; {round(variable[j]['Pos - 97_5'].values[0], 2)})"]
        df = pd.DataFrame(dic)
        fig = px.scatter(df, x="Variable", y="Data", color="Status", error_y="Error", error_y_minus="Error_minus",
                         text="Text", labels={"Text": "Variable", "Data": ""},
                         hover_data={"Data": ":.2f"})

        fig.update_traces(mode="markers")
        fig.layout = self.layout()
        fig.layout.title.text = f"{self.obj.name} - {self.data_type.title()}"
        return fig, df
