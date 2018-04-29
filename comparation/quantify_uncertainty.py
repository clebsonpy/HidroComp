from abc import ABCMeta, abstractmethod


class QuantifyUncertainty(object, metaclass=ABCMeta):

    def __init__(self, reference, compared):
        self.reference
        self.compared

    @abstractmethod
    def quantify(self):
        pass
