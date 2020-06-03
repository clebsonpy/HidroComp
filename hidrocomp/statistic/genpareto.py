import numpy as np

from hidrocomp import statistic as e
from hidrocomp.statistic.stats_build import StatsBuild
from scipy.stats import genpareto
from lmoments3.distr import gpa


class Gpa(StatsBuild):

    name = 'GPA'
    estimator = None
    parameter = {'shape': None, 'loc': None, 'scale': None}

    def __init__(self, data=None,  shape=None, loc=None, scale=None):
        self.shape = shape
        self.loc = loc
        self.scale = scale
        self.parameter['shape'] = self.shape
        self.parameter['loc'] = self.loc
        self.parameter['scale'] = self.scale
        super().__init__(data, shape, loc, scale)
        self.dist = genpareto(c=self.shape, loc=self.loc, scale=self.scale)
    
    def mml(self):
        if self.data is None:
            raise e.DataNotExist("Data not's None", 25)
        mml = gpa.lmom_fit(self.data)
        self.estimador = 'MML'
        self.shape = mml['c']
        self.loc = mml['loc']
        self.scale = mml['scale']
        self.dist = genpareto(c=self.shape, loc=self.loc, scale=self.scale)

        return self.shape, self.loc, self.scale

    def mvs(self):
        if self.data is None:
            raise e.DataNotExist("Data not's None", 35)
        mvs = genpareto.fit(data=self.data)
        self.estimador = 'MVS'
        self.shape = mvs[0]
        self.loc = mvs[1]
        self.scale = mvs[2]
        self.dist = genpareto(c=self.shape, loc=self.loc, scale=self.scale)

        return self.shape, self.loc, self.scale
