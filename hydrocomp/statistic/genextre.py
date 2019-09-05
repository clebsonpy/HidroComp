import numpy as np

from hydrocomp import statistic as e
from hydrocomp.statistic.stats_build import StatsBuild
from scipy.stats import genextreme
from lmoments3.distr import gev


class Gev(StatsBuild):

    name = 'GEV'
    estimador = None
    dist = genextreme

    def __init__(self, data=None,  shape=None, loc=None, scale=None):
        super().__init__(data,  shape, loc, scale)
            
    def mml(self):
        if self.data is None:
            raise e.DataNotExist("Data not's None", 25)
        mml = gev.lmom_fit(self.data)
        self.estimador = 'MML'
        self.shape = mml['c']
        self.loc = mml['loc']
        self.scale = mml['scale']
        self.dist = genextreme(c=self.shape, loc=self.loc, scale=self.scale)

        return self.shape, self.loc, self.scale

    def mvs(self):
        if self.data is None:
            raise e.DataNotExist("Data not's None", 35)
        mvs = genextreme.fit(data=self.data)
        self.estimador = 'MVS'
        self.shape = mvs[0]
        self.loc = mvs[1]
        self.scale = mvs[2]
        self.dist = genextreme(c=self.shape, loc=self.loc, scale=self.scale)

        return self.shape, self.loc, self.scale

    def probs(self, x):
        if self.dist is None:
            raise e.DistributionNotExist('Distribuição não existe', 51)
        else:
            if type(x) is list:
                return [self.probs(i) for i in x]
            return self.dist.cdf(x)

    def values(self, p):
        if self.dist is None:
            raise e.DistributionNotExist('Distribuição não existe', 51)
        else:
            if type(p) is list or type(p) is np.ndarray:
                return [self.values(i) for i in p]
            return self.dist.ppf(p)

    def interval(self, alpha):
        if self.dist is None:
            raise e.DistributionNotExist('Distribuição não existe', 51)
        else:
            return self.dist.interval(alpha)

    def rvs(self, n):
        return self.values(np.random.random(n))
