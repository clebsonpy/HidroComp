import plotly.graph_objs as go


class Graphics:

    def __init__(self, data_group, status, width=None, height=None):
        self.data = data_group
        self.status = status
        self.width = width
        self.height = height

    def plot(self, metric, line=None):
        bandxaxis = go.layout.XAxis(title="Ano")
        bandyaxis = go.layout.YAxis(title="Vazão(m³/s)")

        layout = dict(title=metric.title(),
                      width=self.width, height=self.height,
                      xaxis=bandxaxis, yaxis=bandyaxis,
                      font=dict(family='Time New Roman', color='rgb(0,0,0)')
                      )

        data = list()
        data.append(self._plot_iha(metric))
        try:
            print(line)
            for i in line:
                data.append(self._plot_rva(line=line[i], metric=metric))
        except:
            pass

        fig = dict(data=data, layout=layout)
        return fig, data

    def _plot_rva(self, metric, line):
        line_graph = go.Scatter(x=self.data.index,
                                y=[line[metric]] * len(self.data.index),
                                name='RVA_'+line.name.split('_')[0],
                                mode='lines',
                                line=dict(width=1, color='rgb(0, 0, 0)'),
                                opacity=1, connectgaps=False)
        return line_graph

    def _plot_iha(self, metric):
        point = go.Scatter(x=self.data[metric].index,
                           y=self.data[metric].loc[self.data.index].values,
                           name=self.status.title()+'-impacto',
                           mode='markers+lines',
                           marker=dict(size=8, color='rgb(128, 128, 128)', line=dict(width=1, color='rgb(0, 0, 0)')))

        return point

    def spells(self):
        pass
