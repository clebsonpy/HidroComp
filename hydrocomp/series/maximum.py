import pandas as pd
import plotly as py
import scipy.stats as stat
from hydrocomp.statistic.genextre import Gev

from hydrocomp.graphics.genextreme import GenExtreme
from hydrocomp.graphics.hydrogram_annual import HydrogramAnnual


class Maximum(object):
    distribution = 'GEV'

    def __init__(self, obj, station):
        self.obj = obj
        # self.data = self.obj.data
        self.station = station
        self.peaks = self.__annual()
        self.dist_gev = Gev(self.peaks['peaks'].values)

    def __annual(self):
        self.obj.month_start_year_hydrologic()
        data_by_year_hydrologic = self.obj.data.groupby(pd.Grouper(freq=self.obj.month_abr))
        max_vazao = data_by_year_hydrologic[self.station].max().values
        idx_vazao = data_by_year_hydrologic[self.station].idxmax().values

        self.peaks = pd.DataFrame(max_vazao, index=idx_vazao, columns=['peaks'])
        return self.peaks

    def magnitude(self, period_return, estimador):
        if estimador == 'MML':
            self.dist_gev.mml()
        elif estimador == 'MVS':
            self.dist_gev.mvs()

        p = 1 / period_return
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

    def hydrogram(self, save=False, width=None, height=None, size_text=None, title=None):
        hydrogrm = HydrogramAnnual(data=self.obj.data[self.station], peaks=self.peaks, width=height, height=width,
                                   size_text=size_text, title=title)
        fig, data = hydrogrm.plot()
        if save:
            py.image.save_as(fig, filename='gráficos/hidrogama_maximas_anuais.png')

        return fig, data
