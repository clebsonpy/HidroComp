import pandas as pd

from abc import ABCMeta, abstractmethod


class QuantifyUncertainty(object, metaclass=ABCMeta):

    def __init__(self, reference, compared):
        """Dados de entrada:
            reference: <pd.DataFrame> com as magnitudes estimadas pela distribuiçao
            de referência.
            compared: <dict> contendo os <pd.DataFrame> com as magnitudes estimadas
            pelas distribuições a serem comparadas.
        """
        self.reference = reference
        self.compared = compared

    @abstractmethod
    def calculo_erro(self):
        pass

    def quantify(self):
        df_comp = pd.DataFrame()
        serie_comp = self.calculo_erro()

        df_comp = serie_comp.to_frame()

        return df_comp
