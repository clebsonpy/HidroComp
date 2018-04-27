import scipy.stats as stat
import pandas as pd

from abc import ABCMeta, abstractmethod


class DistributionBiuld(object):

    __metaclass__ = ABCMeta

    def __init__(self, title, forma, localizacao, escala):
        self.title = title
        self.forma = forma
        self.localizacao = localizacao
        self.escala = escala

    def plot(self, type_function):
        if type_function == 'density':
            return self.density()
        elif type_function == 'cumulative':
            return self.cumulative()

    def _data(self, type_function):
        if type_function == 'density':
            return self.__data_density()
        elif type_function == 'cumulative':
            return self.__data_cumulative()

    def __data_cumulative(self):
        probability = []
        for i in range(1, 1000):
            probability.append(i/1000)

        quantiles = stat.genpareto.ppf(probability, self.forma,
                                        loc=self.localizacao,
                                        scale=self.escala)

        dic = {'Vazao': quantiles, 'Probabilidade': probability}

        return pd.DataFrame(dic)

    def __data_density(self):

        cumulative = self.__data_cumulative()

        density = stat.genpareto.pdf(cumulative['Vazao'].values, self.forma,
                                 loc=self.localizacao, scale=self.escala)

        dic = {'Vazao': cumulative['Vazao'].values, 'Densidade': density}

        return pd.DataFrame(dic)

    @abstractmethod
    def cumulative(self):
        pass

    @abstractmethod
    def density(self):
        pass
