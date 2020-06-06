import plotly.graph_objs as go


class ComparationDistribution(object):

    def __init__(self, datas, name, type_function=None):
        self.datas = datas
        self.type_function = type_function
        self.name = name

    def plot(self):
        bandxaxis = go.layout.XAxis(title="Vazão(m³/s)")
        bandyaxis = go.layout.YAxis(title="")

        layout = dict(title="Probabilidade Acumulada",
                      showlegend=True,
                      width=1890, height=827,
                      xaxis=bandxaxis,
                      yaxis=bandyaxis,
                      font=dict(family='Time New Roman', size=28, color='rgb(0,0,0)'))

        fig = dict(data=self.datas, layout=layout)
        return fig, self.datas
