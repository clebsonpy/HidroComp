import pandas as pd
import plotly.graph_objs as go
from plotly import express as exp


class MonthlyCumulativeRainfall:

    def __init__(self, rainfall, station):
        self.rainfall = rainfall
        self.station = station
        self.__events = pd.Series(dtype='float64', name='Monthly')

    @property
    def events(self) -> pd.Series:
        if self.__events.name == self.station:
            return self.__events
        print(self.rainfall.data)
        monthly = self.rainfall.data.groupby(pd.Grouper(freq="M")).sum()[self.station]
        self.__events = monthly

        return self.events

    def plot(self, title, size_text=14, showlegend=True, width=None, height=None):
        bandxaxis = go.layout.XAxis(title='Data')
        bandyaxis = go.layout.YAxis(title='Precipitação (mm)')
        layout = self.__layout(bandyaxis=bandyaxis, bandxaxis=bandxaxis, showlegend=showlegend,
                               size_text=size_text, title=title, width=width, height=height)
        fig = exp.bar(x=self.events.index, y=self.events)
        fig['data'][0]['marker']['color'] = 'rgb(0,0,0)'
        fig.layout = layout
        return fig

    @staticmethod
    def __layout(bandxaxis, bandyaxis, showlegend, title, size_text, width, height):
        layout = dict(
            title=dict(text=title, x=0.5, xanchor='center', y=0.95, yanchor='top',
                       font=dict(family='Courier New, monospace', size=size_text + 10)),
            xaxis=bandxaxis,
            yaxis=bandyaxis,
            width=width, height=height,
            font=dict(family='Courier New, monospace', size=size_text, color='rgb(0,0,0)'),
            showlegend=showlegend, plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF')

        return layout
