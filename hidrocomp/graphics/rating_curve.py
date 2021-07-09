import plotly.graph_objs as go
import numpy as np
import pandas as pd


class RatingCurve:

    def __init__(self, data: pd.DataFrame, title=None, width=None, height=None, size_text=None):
        self.data = data
        self.width = width
        self.height = height
        self.size_text = size_text
        self.title = title

    def plot(self):
        bandxaxis = go.layout.XAxis(title="% do tempo que a vazão é igualada ou superada")
        bandyaxis = go.layout.YAxis(title="Vazão(m³/s)")

        layout = dict(
            title=dict(text=self.title, x=0.5, xanchor='center', y=0.95, yanchor='top',
                       font=dict(family='Courier New, monospace', size=self.size_text + 10)),
            xaxis=bandxaxis,
            yaxis=bandyaxis,
            width=self.width, height=self.height,
            font=dict(family='Courier New, monospace', size=self.size_text, color='rgb(0,0,0)'),
            showlegend=False, plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF')

        data = list()
        data.append(self.data_plot(color='rgb(0,0,0)'))
        fig = dict(data=data, layout=layout)
        return fig, data

    def data_plot(self, color):
        data_y = np.sort(self.data.values)
        count = 0
        data_x = []
        for _ in data_y:
            count += 1
            data_x.append((1-(count/len(data_y)))*100)

        data = go.Scatter(x=data_x,
                          y=data_y,
                          line=dict(width=1, color=color),
                          opacity=1, connectgaps=False)
        return data
