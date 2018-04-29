from abc import ABCMeta, abstractmethod


class QuantifyUncertainty(object, metaclass=ABCMeta):

    def __init__(self, reference, compared):
        self.reference = reference
        self.compared = compared

    @abstractmethod
    def resample_quantify(self):
        pass

    def quantify(self):
        pass
