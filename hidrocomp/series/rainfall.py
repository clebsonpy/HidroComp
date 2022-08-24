import os

import pandas as pd
import plotly.graph_objs as go
from plotly import express as exp

from hidrocomp.series.series_build import SeriesBuild
from hidrocomp.series.monthly_cumulative import MonthlyCumulativeRainfall
from hidrocomp.series.minimum import MinimumRainfall
from hidrocomp.series.maximum import MaximumRainfall
from hidrocomp.graphics.hydrogram_clean import HydrogramClean


class Rainfall(SeriesBuild):

    type_data = 'PLUVIOMÉTRICO'
    data_type = 'rainfall'

    def __init__(self, data=None, path_file=None, station=None, source=None, *args, **kwargs):
        super().__init__(data=data, path=path_file, station=station, source=source, type_data=self.type_data, *args,
                         **kwargs)

    def _month_start_year_hydrologic(self):
        pass

    def monthly_cumulative(self):
        monthly_cumulative = MonthlyCumulativeRainfall(rainfall=self, station=self.station)
        return monthly_cumulative

    def minimum(self):
        minimum = MinimumRainfall(rainfall=self, station=self.station)
        return minimum

    def maximum(self):
        maximum = MaximumRainfall(rainfall=self, station=self.station)
        return maximum

    def plot_annual_anomaly(self, title, size_text=14, showlegend=True, width=None, height=None):
        annual_sum = self.data.groupby(pd.Grouper(freq='A')).sum()
        annual_mean = self.data.groupby(pd.Grouper(freq='A')).sum().mean()

        anomaly = annual_sum - annual_mean
        anomaly = anomaly.loc[anomaly.index[1]:anomaly.index[-2]]

        anomaly['color'] = 'black'


        bandxaxis = go.layout.XAxis(title='Data')
        bandyaxis = go.layout.YAxis(title='Precipitação (mm)')
        layout = self.__layout(bandyaxis=bandyaxis, bandxaxis=bandxaxis, showlegend=showlegend,
                               size_text=size_text, title=title, width=width, height=height)
        fig = exp.bar(anomaly, x=anomaly.index, y=self.station)
        fig.layout = layout
        fig.update_traces(marker_color='black')
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

    def hietogram(self, title, threshold=None, width=None, height=None, size_text=16, **kwargs):
        if self.station is None:
            hietogram = HydrogramClean(self.data, threshold=threshold, width=width, height=height, size_text=size_text,
                                       title=title, data_type=self.data_type, **kwargs)
            fig, data = hietogram.plot()
        else:
            hietogram = HydrogramClean(self.data[self.station], threshold=threshold, width=width, height=height,
                                       size_text=size_text, title=title, data_type=self.data_type, **kwargs)
            fig, data = hietogram.plot()
        return fig, data
