import pandas as pd
import scipy.stats as stat
from lmoments3 import distr

from graphics.genextreme import GenExtreme
from graphics.hydrogram_annual import HydrogramAnnual


class Maximum(object):

    distribution = 'GEV'

    def __init__(self, obj, station):
        self.obj = obj
        self.data = self.obj.data
        self.station = station

    def annual(self):
        data_by_year_hydrologic = self.data.groupby(pd.Grouper(
            freq='AS-%s' % self.obj.month_start_year_hydrologic(self.station)[1]))
        max_vazao = data_by_year_hydrologic[self.station].max().values
        idx_vazao = data_by_year_hydrologic[self.station].idxmax().values

        self.peaks = pd.DataFrame(max_vazao, index=idx_vazao, columns=['Vazao'])
        return self.peaks

    def mml(self):
        try:
            peaks = self.peaks.copy()
            mom = distr.gev.lmom_fit(peaks['Vazao'].values)
            para = [mom['c'], mom['loc'], mom['scale']]
            return para
        except AttributeError:
            self.annual()
            return self.mml()

    def mvs(self):
        try:
            peaks = self.peaks['Vazao'].values.copy()
            para = stat.genextreme.fit(sorted(peaks))
            return para
        except AttributeError:
            self.annual()
            return self.mvs()
            #self.para = stat.genextreme.fit(self.peaks['Vazao'].values)

    def plot_distribution(self, title, estimador, type_function):
        if estimador == 'mvs':
            para = self.mvs()
        elif estimador == 'mml':
            para = self.mml()
        else:
            raise ValueError
        genextreme = GenExtreme(title, para[0], para[1], para[2])
        genextreme.plot(type_function)
        #genextreme = GenExtreme(title, self.para[0], self.para[1], self.para[2])
        #genextreme.plot(type_function)

    def plot_hydrogram(self):
        print('Aqui')
        self.annual()
        hydrogrm = HydrogramAnnual(data=self.data[self.station],
                                   peaks=self.peaks)
        hydrogrm.plot()
