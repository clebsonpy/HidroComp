import pandas as pd
import plotly as py
import scipy.stats as stat
from hidrocomp.statistic.genextre import Gev

from hidrocomp.graphics.genextreme import GenExtreme
from hidrocomp.graphics.hydrogram_annual import HydrogramAnnual
from hidrocomp.graphics.polar import Polar


class Maximum(object):
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
        return self.peaks

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
