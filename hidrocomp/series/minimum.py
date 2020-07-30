import pandas as pd
import plotly as py
from hidrocomp.statistic.genextre import Gev

from hidrocomp.graphics.genextreme import GenExtreme
from hidrocomp.graphics.hydrogram_annual import HydrogramAnnual
from hidrocomp.graphics.polar import Polar


class Minimum(object):
    distribution = 'GEV'

    def __init__(self, obj, station):
        self.obj = obj
        self.station = station
        self.peaks = self.__annual()
        self.dist_gev = Gev(self.peaks['peaks'].values)

    def __annual(self):
        data_by_year_hydrologic = self.obj.data.groupby(pd.Grouper(freq=self.obj.month_abr_drought))
        min = data_by_year_hydrologic[self.station].min()
        idx = data_by_year_hydrologic[self.station].idxmin()
        min_vazao = min.values
        idx_vazao = idx.values
        self.peaks = pd.DataFrame(min_vazao, index=idx_vazao, columns=['peaks'])
        return self.peaks

    def magnitude(self, period_return, estimador):
        if estimador == 'MML':
            self.dist_gev.mml()
        elif estimador == 'MVS':
            self.dist_gev.mvs()

        p = 1-(1 / period_return)
        return self.dist_gev.values(p)

    def plot_distribution(self, title, estimador, type_function, save=False):
        if estimador == 'MVS':
            self.dist_gev.mvs()
        elif estimador == 'MML':
            self.dist_gev.mml()
        else:
            raise ValueError("Estimador: [mvs or mml]")
        genextreme = GenExtreme(title, self.dist_gev.shape, self.dist_gev.loc, self.dist_gev.scale)
        data, fig = genextreme.plot(type_function)
        if save:
            py.image.save_as(fig, filename='gráficos/GEV_%s_%s.png' % (type_function,
                                                                       estimador))
        return fig, data

    def hydrogram(self, save=False, width=None, height=None, size_text=16, title=None):
        _hydrogram = HydrogramAnnual(data=self.obj.data[self.station], peaks=self.peaks, width=height, height=width,
                                     size_text=size_text, title=title, station=self.station)
        fig, data = _hydrogram.plot()
        if save:
            py.image.save_as(fig, filename='gráficos/hidrogama_maximas_anuais.png')

        return fig, data

    def polar(self, save=False, width=None, height=None, size_text=14, title="Máximas Anuais"):
        _polar = Polar(df_events=self.peaks)
        fig, data = _polar.plot(width=width, height=height, size_text=size_text, title=title)
        if save:
            py.image.save_as(fig, filename='graficos/polar_maximas_anuais.png')

        return fig, data
