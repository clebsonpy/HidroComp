import scipy.stats as stat

from abc import ABCMeta, abstractmethod


class DistributionBiuld(object, metaclass=ABCMeta):

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
            return self._data_density()
        elif type_function == 'cumulative':
            return self._data_cumulative()

    @abstractmethod
    def _data_cumulative(self):
        pass

    @abstractmethod
    def _data_density(self):
        pass

    @abstractmethod
    def cumulative(self):
        pass

    @abstractmethod
    def density(self):
        pass
