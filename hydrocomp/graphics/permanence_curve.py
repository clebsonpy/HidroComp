import plotly.graph_objs as go
import numpy as np


class PermanenceCurve:

    def __init__(self, data, width=None, height=None, size_text=None, title=None):
        self.data = data
        self.width = width
        self.height = height
        self.size_text = size_text
        self.title = title

    def plot(self):
        bandxaxis = go.layout.XAxis(title="Probabilidade de excedência")
        bandyaxis = go.layout.YAxis(title="Vazão(m³/s)")


        layout = dict(title=self.title,
                      width=self.width, height=self.height,
                      xaxis=bandxaxis, yaxis=bandyaxis,
                      font=dict(family='Time New Roman', size=self.size_text, color='rgb(0,0,0)')
                      )

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