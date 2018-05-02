import pandas as pd

from comparasion.mae import MAE
from comparasion.quantify_uncertainty import QuantifyUncertainty


class RMAE(QuantifyUncertainty):
    """
    Relative Mean Absolute Error - RMAE
    RMAE = MAE/mean(Qmax)
    """
    name = 'RMAE'
    def __init__(self, reference, compared):
        super().__init__(reference, compared, self.name)

    def formula(self, reference, compared):
        soma = 0
        for i in compared:
            soma += abs(i - reference)

        n = len(compared)
        mae = (1/n) * soma

        return mae/reference

    def calculo_erro(self, compared):
        mae = MAE(self.reference, compared).quantify()
        rmae = []
        prob = []
        soma = 0
        for i in self.reference.index:
            prob.append(i)
            aux = mae[compared.name][i] / self.reference[i]
            soma += aux

            rmae.append(aux)

        rmae_value = (1/len(self.reference)*soma)
        rmae.append(rmae_value)
        prob.append('RMAE')
        rmae_serie = pd.Series(rmae, index=prob, name=compared.name)
        return rmae_serie
