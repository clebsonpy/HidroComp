import pandas as pd

from abc import ABCMeta, abstractmethod


class QuantifyUncertainty(object, metaclass=ABCMeta):

    def __init__(self, reference, compared, name):
        """Dados de entrada:
            reference: <pd.DataFrame> com as magnitudes estimadas pela distribuiçao
            de referência.
            compared: <dict> contendo os <pd.DataFrame> com as magnitudes estimadas
            pelas distribuições a serem comparadas.
        """
        self.reference = reference
        self.compared = compared
        self.name = name

    @abstractmethod
    def calculo_erro(self, compared):
        pass

    @abstractmethod
    def formula(self, arg):
        pass

    def quantify_resample(self):
        prob = []
        comp = []
        for i in self.reference.index:
            comp.append(self.formula(self.reference[i], self.compared[i]))
            prob.append(i)

        return pd.DataFrame(comp, index=prob, columns=[self.name])

    def quantify(self):
        df_comp = pd.DataFrame()
        try:
            if type(self.compared) is type(pd.Series()):
                raise TypeError

            for comp in self.compared:
                self.compared = comp
                df_comp = df_comp.combine_first(self.quantify())

        except TypeError:
            serie_comp = self.calculo_erro(self.compared)
            df_comp = serie_comp.to_frame()

        return df_comp
