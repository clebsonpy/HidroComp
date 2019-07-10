import numpy

from statistic.stats_build import StatsBuild
from scipy.stats import genextreme
from lmoments3.distr import gev

class Gev(StatsBuild):

    estimadores = ['mvs', 'mml']

    def __init__(self, data=None,  shape=None, loc=None, scale=None):
        if data is None:
            if shape is None or loc is None or scale is None:
                raise ValueError("Parâmetros não  informados")
            else:
                self.shape = shape
                self.loc = loc
                self.scale = scale
        else:
            self.data = data

    def mml(self):
        if self.data is None:
            raise ValueError("Data not's None")
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

    def prob(self, x, estimador):
        try:
            return genextreme.cdf(x, c=self.shape, loc=self.loc, scale=self.scale)
        except AttributeError:
            if estimador not in self.estimadores:
                raise ValueError('Estimador não existe')
            else:
                eval('self.' + estimador)()
            return self.prob(x, estimador=estimador) 

    def value(self, p, estimador=None):
        try:
            return genextreme.ppf(p, c=self.shape, loc=self.loc, scale=self.scale)
        except AttributeError:
            if estimador not in self.estimadores:
                raise ValueError('Estimador não existe')
            else:
                eval('self.' + estimador)()
            return self.value(p, estimador=estimador)
        

    def interval(self, alpha):
        inteval = genextreme.interval(alpha, c=self.shape, loc=self.loc, scale=self.scale)
        return inteval

    def plot_cdf(self):
        pass

    def plot_pdf(self):
        pass
