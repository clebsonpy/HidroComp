from abc import ABCMeta, abstractmethod


class BootstrapBuild(object, metaclass=ABCMeta):

    def __init__(self, forma, localizacao, escala, tamanho):
        self.forma = forma
        self.localizacao = localizacao
        self.escala = escala
        self.tamanho = tamanho

    @abstractmethod
    def fit_resample(self):
        pass

    @abstractmethod
    def fits_resamples(self, quantidade):
        pass

    @abstractmethod
    def magnitudes_resamples(self, quantidade):
        pass
