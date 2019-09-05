from abc import ABCMeta, abstractmethod

class DistributionBiuld(object, metaclass=ABCMeta):

    def __init__(self, title, shape, location, scale):
        self.title = title
        self.shape = shape
        self.location = location
        self.scale = scale

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
