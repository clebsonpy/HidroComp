from .hydrogram_build import HydrogramBuild
import plotly.graph_objs as go
import pandas as pd


class HydrogramYear(HydrogramBuild):

    def __init__(self, data, width=None, height=None, size_text=None, title=None):
        self.data = data
        super().__init__(width=width, height=height, size_text=size_text, title=title)

    def plot(self):
        group = self.group_by_year()

        trace = []
        for g in group:
            trace.append(go.Scatter(
                x=group[g].index,
                y=group[g].values,
                mode="lines",
                name=g,)
            )
    
        data = trace
        bandxaxis = go.layout.XAxis(
            title="Mês",
            tickformat="%b",
        )

        bandyaxis = go.layout.YAxis(
            title="Vazão(m³/s)",
        )

        layout = dict(
            title=self.title,
            xaxis=bandxaxis,
            yaxis=bandyaxis,
            width=self.width, height=self.height,
            font=dict(family='Courier New, monospace', size=self.size_text, color='#7f7f7f'))

        fig = dict(data=data, layout=layout)

        return fig

    def group_by_year(self):
        list_year = []
        for key, data in self.data:
            aux = data.values.T
            index = data.index
            indexN = [pd.to_datetime('%s/%s/%s' % (i.month, i.day, 1998)) if i.month >= key.month else pd.to_datetime(
                '%s/%s/%s' % (i.month, i.day, 1999)) for i in index]
            serie = pd.Series(aux[0], index=indexN, name=key.year)
            list_year.append(serie)
        return pd.DataFrame(list_year).T