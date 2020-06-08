import plotly.graph_objs as go
import pandas as pd


class Graphics:

    def __init__(self, data_variable, status, width=None, height=None, size_text=14):
        self.data = data_variable.sort_index()
        self.name = data_variable.name
        self.status = status
        self.width = width
        self.height = height
        self.size_text = size_text

    def plot(self, metric, line=None, color=None):
        bandxaxis = go.layout.XAxis(title="Ano")
        bandyaxis = go.layout.YAxis(title="")
        layout = self.layout(bandxaxis=bandxaxis, bandyaxis=bandyaxis)

        data = list()
        data.append(self._plot_iha(color))
        try:
            for i in line:
                if i != 'median_line':
                    data.append(self._plot_rva(line=line[i], metric=metric))
        except:
            pass

        fig = dict(data=data, layout=layout)
        return fig, data

    def _plot_rva(self, metric, line):
        line_graph = go.Scatter(x=self.data.index,
                                y=[line[metric]] * len(self.data.index),
                                name="RVA targets",
                                mode='lines',
                                line=dict(width=1, color='rgb(0, 0, 0)'),
                                opacity=1, connectgaps=False)
        return line_graph

    def _plot_iha(self, color):
        point = go.Scatter(x=self.data.index,
                           y=self.data.loc[self.data.index].values,
                           name=self.status.title()+'-impacto',
                           mode='markers+lines',
                           marker=dict(size=8, color=color, line=dict(width=1, color=color)))

        return point

    def layout(self, bandxaxis, bandyaxis):
        layout = dict(
            title=dict(text=self.name, x=0.5, xanchor='center', y=0.95, yanchor='top',
                       font=dict(family='Courier New, monospace', size=self.size_text + 10)),
            xaxis=bandxaxis,
            yaxis=bandyaxis,
            width=self.width, height=self.height,
            font=dict(family='Courier New, monospace', size=self.size_text, color='rgb(0,0,0)'),
            showlegend=True, plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF')

        return layout