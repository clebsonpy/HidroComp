import numpy as np

from hidrocomp import statistic as e
from hidrocomp.statistic.stats_build import StatsBuild
from scipy.stats import pearson3
from lmoments3.distr import pe3


class Pearson3(StatsBuild):

    name = 'Pearson3'
    estimator = None
    parameter = {'loc': None, 'scale': None}

    def __init__(self, data=None,  loc=None, scale=None):
        self.loc = loc
        self.scale = scale
        self.parameter['loc'] = self.loc
        self.parameter['scale'] = self.scale
        super().__init__(data, loc, scale)
        self.dist = pearson3(loc=self.loc, scale=self.scale, skew=0.1)

    def mml(self):
        if self.data is None:
            raise e.DataNotExist("Data not's None", 25)
        mml = pe3.lmom_fit(self.data)
        self.estimador = 'MML'
        self.loc = mml['loc']
        self.scale = mml['scale']
        self.dist = pearson3(loc=self.loc, scale=self.scale, skew=0.1)
        return self.loc, self.scale

    def mvs(self):
        if self.data is None:
            raise e.DataNotExist("Data not's None", 35)
        mvs = pearson3.fit(data=self.data)
        self.estimador = 'MVS'
        self.loc = mvs[0]
        self.scale = mvs[1]
        self.dist = pearson3(loc=self.loc, scale=self.scale, skew=0.1)

        return self.loc, self.scale
