import pandas as pd
import plotly as py
import plotly.graph_objs as go
from plotly import express as exp
import scipy.stats as stat
from hidrocomp.statistic.genextre import Gev

from hidrocomp.graphics.genextreme import GenExtreme
from hidrocomp.graphics.hydrogram_annual import HydrogramAnnual
from hidrocomp.graphics.polar import Polar


class MaximumFlow(object):
    distribution = 'GEV'

    def __init__(self, obj, station):
        self.obj = obj
        self.station = station
        self.peaks = self.__annual()
        self.dist_gev = Gev(self.peaks['Peaks'])

    def __annual(self):
        data_by_year_hydrologic = self.obj.data.groupby(pd.Grouper(freq=self.obj.month_abr_flood))
        max = data_by_year_hydrologic[self.station].max()
        idx = data_by_year_hydrologic[self.station].idxmax()
        max_vazao = max.values
        idx_vazao = idx.values
        self.peaks = pd.DataFrame(max_vazao, index=idx_vazao, columns=['Peaks'])
        return self.peaks.dropna(axis=0)

    def period_return(self, magnitude, estimador):
        if estimador == 'MML':
            self.dist_gev.mml()
        elif estimador == 'MVS':
            self.dist_gev.mvs()

        p = self.dist_gev.probs(magnitude)
        return 1/(1-p)

    def magnitude(self, period_return, estimador):
        if estimador == 'MML':
            self.dist_gev.mml()
        elif estimador == 'MVS':
            self.dist_gev.mvs()

        p = 1-(1 / period_return)
        return self.dist_gev.values(p)

    def plot_distribution(self, title, estimador, type_function, save=False):
        if estimador.upper() == 'MVS':
            self.dist_gev.mvs()
        elif estimador.upper() == 'MML':
            self.dist_gev.mml()
        else:
            raise ValueError("Estimador: [mvs or mml]")
        genextreme = GenExtreme(title, self.dist_gev.shape, self.dist_gev.loc, self.dist_gev.scale)
        fig, data = genextreme.plot(type_function)
        if save:
            py.image.save_as(fig, filename='gráficos/GEV_%s_%s.png' % (type_function, estimador))
        return fig, data

    def hydrogram(self, save=False, width: int = None, height: int = None, size_text: int = 16,
                  title=None, showlegend: bool = True, language: str = 'pt'):
        _hydrogram = HydrogramAnnual(data=self.obj.data[self.station], peaks=self.peaks, width=height, height=width,
                                     size_text=size_text, title=title, station=self.station, language=language,
                                     showlegend=showlegend, data_type=self.obj.data_type)
        fig, data = _hydrogram.plot()
        if save:
            py.image.save_as(fig, filename='gráficos/hidrogama_maximas_anuais.png')

        return fig, data

    def polar(self, save=False, width=None, height=None, size_text=14, title="Máximas Anuais", language: str = 'pt',
              color=None, name=None, showlegend: bool = False):
        _polar = Polar(df_events=self.peaks)
        fig, data = _polar.plot(width=width, height=height, size_text=size_text, title=title, language=language,
                                color=color, name=name, showlegend=showlegend)
        if save:
            py.image.save_as(fig, filename='graficos/polar_maximas_anuais.png')

        return fig, data


class MaximumRainfall(object):
    # distribution = 'GEV'

    def __init__(self, rainfall, station):
        self.rainfall = rainfall
        self.station = station
        self.peaks = self.__annual()

    def __annual(self):
        data_by_year_hydrologic = self.rainfall.data.groupby(pd.Grouper(freq='A-JAN'))
        max = data_by_year_hydrologic[self.station].max()
        idx = data_by_year_hydrologic[self.station].idxmax()
        max_vazao = max.values
        idx_vazao = idx.values
        self.peaks = pd.DataFrame(max_vazao, index=idx_vazao, columns=['Peaks'])
        return self.peaks.dropna(axis=0)

    def magnitude(self, period_return, estimador):
        pass

    def plot_distribution(self, title, estimador, type_function, save=False):
        pass

    def plot(self, title, size_text=14, showlegend=True, width=None, height=None):
        bandxaxis = go.layout.XAxis(title='Data')
        bandyaxis = go.layout.YAxis(title='Precipitação (mm)')
        layout = self.__layout(bandyaxis=bandyaxis, bandxaxis=bandxaxis, showlegend=showlegend,
                               size_text=size_text, title=title, width=width, height=height)
        fig = exp.line(x=self.peaks.index.values, y=self.peaks['Peaks'].values)
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