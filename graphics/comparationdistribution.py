import plotly.graph_objs as go


class ComparationDistribution(object):

    def __init__(self, datas, type_function, name):
        self.datas = datas
        self.type_function = type_function
        self.name = name

    def plot(self):
        bandxaxis = go.XAxis(title="Vazão(m³/s)")
        bandyaxis = go.YAxis(title="")

        layout = dict(title="Probabilidade Acumulada",
                      showlegend=True,
                      width=945, height=827,
                      xaxis=bandxaxis,
                      yaxis=bandyaxis,
                      font=dict(family='Time New Roman', size=34, color='rgb(0,0,0)'))

        fig = dict(data=self.datas, layout=layout)
        return self.datas, fig
