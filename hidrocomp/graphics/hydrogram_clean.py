import pandas as pd
import plotly.graph_objs as go
from hidrocomp.graphics.hydrogram_build import HydrogramBuild


class HydrogramClean(HydrogramBuild):

    def __init__(self, data, threshold=None, width=None, height=None, size_text=None, title=None, y_title=None,
                 x_title=None, color=None):
        super().__init__(width=width, height=height, size_text=size_text, title=title)
        self.threshold = threshold
        self.data = pd.DataFrame(data)
        self.y_title = y_title
        self.x_title = x_title
        self.color = color

    def plot(self):
        bandxaxis = go.layout.XAxis(title=self.x_title)
        bandyaxis = go.layout.YAxis(title=self.y_title)

        if len(self.data.columns.values) == 1:

            layout = dict(
                title=dict(text=self.title, x=0.5, xanchor='center', y=0.95, yanchor='top',
                           font=dict(family='Courier New, monospace', size=self.size_text + 10)),
                xaxis=bandxaxis,
                yaxis=bandyaxis,
                width=self.width, height=self.height,
                font=dict(family='Courier New, monospace', size=self.size_text, color='rgb(0,0,0)'),
                showlegend=True, plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF')

            data = list()
            data.append(self._plot_one(self.data, self.title, color='rgb(0,0,0)'))

            if self.threshold is not None:
                if type(self.threshold) is list:
                    trace_threshold = []
                    i = 1
                    for t in self.threshold:
                        trace_threshold.append(self._plot_threshold(self.data, t, name="Limiar - {}".format(i)))
                        i += 1
                else:
                    trace_threshold = [self._plot_threshold(self.data, self.threshold, name="Limiar")]
                data = data + trace_threshold
            else:
                pass

            fig = dict(data=data, layout=layout)
            return fig, data

        else:

            data, buttons = self._plot_multi()

            if self.threshold is not None:
                if type(self.threshold) is list:
                    trace_threshold = []
                    i = 1
                    for t in self.threshold:
                        trace_threshold.append(self._plot_threshold(self.data, t, name="Threshold - {}".format(i)))
                        i += 1
                else:
                    trace_threshold = [self._plot_threshold(self.data, self.threshold, name="Threshold")]
                data = data + trace_threshold
            else:
                pass

            menus = False
            if menus:
                update_menus = go.layout.Updatemenu(active=0, buttons=list(buttons))
            else:
                update_menus = None

            layout = dict(
                title=dict(text=self.title, x=0.5, xanchor='center', y=0.95, yanchor='top',
                           font=dict(family='Courier New, monospace', size=self.size_text + 10)),
                xaxis=bandxaxis,
                yaxis=bandyaxis,
                width=self.width, height=self.height,
                font=dict(family='Courier New, monospace', size=self.size_text, color='rgb(0,0,0)'),
                showlegend=True, plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF', updatemenus=update_menus)
            fig = dict(data=data, layout=layout)
            return fig, data

    def _plot_threshold(self, group, threshold, name):
        trace_threshold = go.Scatter(
            x=list(group[group.columns[0]].index),
            y=[threshold]*len(group),
            mode='lines',
            name=name,
            textposition='top right',
            line=dict(color='rgb(0, 0, 0)',
                      width=1.5,
                      dash='dot')
        )

        return trace_threshold

    def _plot_multi(self):
        data = []
        buttons = [dict(label="All",
                        method='update',
                        args=[{"visible": [True] * len(self.data.columns)},
                              {"title": "Hidrograma"}]
                        )]
        aux = 0
        visible = [False] * len(self.data.columns)
        for i in self.data:
            visible[aux] = True
            try:
                color = self.color[i]
            except:
                color = None

            data.append(self._plot_one(pd.DataFrame(self.data[i]), station=i, color=color))

            buttons.append(
                dict(label=i,
                     method='update',
                     args=[{"visible": visible},
                           {"title": "Hidrograma: {}".format(i)}]
                     )
            )

            visible = [False] * len(self.data.columns)
            aux += 1
        return data, buttons
