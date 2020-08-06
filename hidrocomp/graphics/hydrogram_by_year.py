from .hydrogram_build import HydrogramBuild
import plotly.graph_objs as go
import pandas as pd
import colorlover as cl
import numpy as np


class HydrogramYear(HydrogramBuild):

    def __init__(self, data, title, threshold, width, height, size_text):
        self.data = data
        self.threshold = threshold
        super().__init__(width=width, height=height, size_text=size_text, title=title)

    def plot(self):
        group = self.group_by_year()
        number_of_lines = len(group.columns)
        ylrd = cl.scales['9']['div']['Spectral']
        ylrd = cl.interp(ylrd, number_of_lines)
        colors = dict(zip(group.columns, ylrd))
        trace = []
        for g in group:
            trace.append(go.Scatter(
                x=group[g].index,
                y=group[g].values,
                mode="lines",
                line=dict(color=colors[g]),
                name=g,)
            )

        colorbar_trace = go.Scatter(x=[None],
                                    y=[None],
                                    mode='markers',
                                    marker=dict(
                                        colorscale=ylrd,
                                        showscale=True,
                                        colorbar=dict(title='Ano'),
                                        cmin=group.columns[0],
                                        cmax=group.columns[-1],
                                    ),
                                    hoverinfo='none',
        )

        if self.threshold is not None:
            if type(self.threshold) is list:
                trace_threshold = []
                i = 1
                for t in self.threshold:
                    trace_threshold.append(self._plot_threshold(group, t, name="Threshold - {}".format(i)))
                    i += 1
            else:
                trace_threshold = [self._plot_threshold(group, self.threshold, name="Threshold")]
            data = trace + [colorbar_trace] + trace_threshold
        else:
            data = trace + [colorbar_trace]

        bandxaxis = go.layout.XAxis(
            title="Month",
            tickformat="%b",
            linecolor='rgba(1,1,1,1)',
            gridcolor='rgba(1,1,1,1)'
        )

        bandyaxis = go.layout.YAxis(
            title="Flow(m³/s)",
            showgrid=False,
        )

        layout = dict(
            title=dict(text=self.title,  x=0.5, xanchor='center', y=0.95, yanchor='top',
                       font=dict(family='Courier New, monospace', color='rgba(0,0,0,0)', size=self.size_text+6)),
            xaxis=bandxaxis,
            yaxis=bandyaxis,
            width=self.width, height=self.height,
            font=dict(family='Courier New, monospace', size=self.size_text, color='#7f7f7f'),
            showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')

        fig = dict(data=data, layout=layout)

        return fig, data

    def _plot_threshold(self, group, threshold, name):
        trace_threshold = go.Scatter(
            x=list(group[group.columns[2]].index),
            y=[threshold]*len(group),
            mode='lines+text',
            text=[name],
            textposition='top right',
            line=dict(color='rgb(0, 0, 0)',
                      width=1.5,
                      dash='dot')
        )

        return trace_threshold


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
