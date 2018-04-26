import pandas as pd
import scipy.stats as stat

from graphics.gev import Gev


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

    def mvs(self):
        try:
            self.fit = stat.genextreme.fit(self.peaks['Vazao'].values)
        except AttributeError:
            self.annual()
            self.fit = stat.genextreme.fit(self.peaks['Vazao'].values)

        return self.fit

    def plot_distribution(self, title, type_function):
        try:
            genextreme = Gev(title, self.fit[0], self.fit[1], self.fit[2])
        except AttributeError:
            self.mvs()
            genextreme = Gev(title, self.fit[0], self.fit[1], self.fit[2]).plot(type_function)
