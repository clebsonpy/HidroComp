import pandas as pd
import scipy.stats as stat


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
            parametros = stat.genpareto.fit(self.peaks['Vazao'].values)
        except AttributeError:
            self.annual()
            parametros = stat.genpareto.fit(self.peaks['Vazao'].values)

        return parametros
