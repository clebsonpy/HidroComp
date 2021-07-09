import numpy as np
from hidrocomp import statistic as e
from hidrocomp.statistic.stats_build import StatsBuild
from scipy.stats import norm


class Normal(StatsBuild):
    name = 'NOR'
    estimador = None
    parameter = {'loc': None, 'scale': None}

    def __init__(self, data: list = None, loc=None, scale=None):
        self.loc = loc
        self.scale = scale
        self.parameter['loc'] = self.loc
        self.parameter['scale'] = self.scale
        super().__init__(data, loc, scale)
        try:
            self.dist = norm(loc=self.loc, scale=self.scale)
        except TypeError:
            self.dist = None

    def z_score(self, q: float) -> float:
        if self.data is not None:
            mean = np.mean(self.data)
            std = np.std(self.data)
        else:
            mean = self.loc
            std = self.scale

        return (q - mean) / std

    def mvs(self):
        if self.data is None:
            raise e.DataNotExist("Data not's None", 35)

        mvs = norm.fit(self.data)
        self.estimador = 'MML'
        self.loc = mvs[0]
        self.scale = mvs[1]
        self.dist = norm(loc=self.loc, scale=self.scale)

        return self.loc, self.scale

    def mml(self):
        if self.data is None:
            raise e.DataNotExist("Data not's None", 39)

        mml = norm.lmom_fit(self.data)
        self.estimador = 'MML'
        self.loc = mml['loc']
        self.scale = mml['scale']
        self.dist = norm(loc=self.loc, scale=self.scale)

        return self.loc, self.scale

    def rvs(self, n):
        pass