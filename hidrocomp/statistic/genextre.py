from hidrocomp import statistic as e
from hidrocomp.statistic.stats_build import StatsBuild
from scipy.stats import genextreme
from lmoments3.distr import gev


class Gev(StatsBuild):

    name = 'GEV'
    estimador = None
    parameter = {'shape': None, 'loc': None, 'scale': None}

    def __init__(self, data=None,  shape=None, loc=None, scale=None):
        self.shape = shape
        self.loc = loc
        self.scale = scale
        self.parameter['shape'] = self.shape
        self.parameter['loc'] = self.loc
        self.parameter['scale'] = self.scale
        super().__init__(data,  shape, loc, scale)
        try:
            self.dist = genextreme(c=self.shape, loc=self.loc, scale=self.scale)
        except TypeError:
            self.dist = None
            
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

    def rvs(self, n):
        pass