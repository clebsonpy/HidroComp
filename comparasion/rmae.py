import pandas as pd

from comparasion.mae import MAE
from comparasion.quantify_uncertainty import QuantifyUncertainty


class RMAE(QuantifyUncertainty):
    """
    Relative Mean Absolute Error - RMSE
    RMAE = MAE/mean(Qmax)
    """
    def __init__(self, reference, compared):
        super().__init__(reference, compared)

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
