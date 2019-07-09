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
        mvs = genextreme.fit(self.data)
        self.shape = mvs[0]
        self.loc = mvs[1]
        self.scale = mvs[2]

        return self.shape, self.loc, self.scale

    def mom(self):
        if self.data is None:
            raise ValueError("Data not's None")
        mom = genextreme.moment(self.data)
        self.shape = mom[0]
        self.loc = mom[1]
        self.scale = mom[2]

        return self.shape, self.loc, self.scale
        
    def prob(self, x):
        p = genextreme.cdf(x, c=self.shape, loc=self.loc, scale=self.scale)
        return p

    def value(self, p):
        x = genextreme.ppf(p, c=self.shape, loc=self.loc, scale=self.scale)
        return x

    def interval(self, alpha):
        inteval = genextreme.interval(alpha, loc=self.loc, scale=self.scale)
        return inteval

    def plot_cdf(self):
        pass

    def plot_pdf(self):
        pass
