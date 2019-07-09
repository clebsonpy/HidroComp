import numpy

from statistic.stats_build import StatsBuild
from scipy.stats import genextreme
from lmoments3.distr import gev

class Gev(StatsBuild):

    def __init__(self, data=None,  shape=None, loc=None, scale=None):
        super().__init__(data)
        self.shape = shape
        self.loc = loc
        self.scale = scale

    def mml(self):
        if self.data is None:
            raise ValueError("Data not's None")

        print(self.data)
        mml = gev.lmom_fit(self.data)
        self.shape = mml['c']
        self.loc = mml['loc']
        self.scale = mml['scale']

        return self.shape, self.loc, self.scale

    def mvs(self):
        if self.data is None:
            raise ValueError("Data not's None")

        self.shape, self.loc, self.scale = genextreme.fit(self.data)

    def mom(self):
        return 'isso'

    def prob(self, x):
        pass

    def value(self, p):
        pass

    def interval(self, alpha):
        pass

    def plot_cdf(self):
        pass

    def plot_pdf(self):
        pass
