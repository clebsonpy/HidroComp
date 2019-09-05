from abc import ABCMeta, abstractmethod


class BootstrapBuild(object, metaclass=ABCMeta):

    def __init__(self, shape, location, scale, size):
        self.shape = shape
        self.location = location
        self.scale = scale
        self.size = size

    @abstractmethod
    def fit_resample(self):
        pass

    @abstractmethod
    def fits_resamples(self, quantity):
        pass

    @abstractmethod
    def magnitudes_resamples(self, quantity):
        pass
