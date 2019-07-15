import numpy

import statistic.exceptions as e
from statistic.stats_build import StatsBuild
from scipy.stats import genextreme
from lmoments3.distr import gev
from graphics.genextreme import GenExtreme

class Gev(StatsBuild):

    name = 'GEV'
    estimador = None

    def __init__(self, data=None,  shape=None, loc=None, scale=None):
        if data is None:
            if shape is None or loc is None or scale is None:
                raise e.DataNotExist("Parâmetros não  informados", 12)
            else:
                self.shape = shape
                self.loc = loc
                self.scale = scale
                self.dist = genextreme(c=self.shape, loc=self.loc, scale=self.scale)
        else:
            self.data = data
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
            if type(p) is list:
                return [self.values(i) for i in p]
            return self.dist.ppf(p)

    def interval(self, alpha):
        if self.dist is None:
            raise e.DistributionNotExist('Distribuição não existe', 51)
        else:
            return self.dist.interval(alpha)


if __name__ == '__main__':
    from statistic.exceptions import DataNotExist
    
    data = [1347,  857, 1626,  977, 1065,  997,  502, 1663,  992, 1487, 1041, 2251, 1110, 1553, 1090, 1268, 1113, 1358,  402]
    
    try:
        dist_gev = Gev()
    except DataNotExist:
        dist_gev = Gev(data=data)
    print(dist_gev.interval(0.75))