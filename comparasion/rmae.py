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

    def calculo_erro(self):
        mae = MAE(self.reference, self.compared).quantify()
        prob = []
        rmae = []
        for i in self.reference.index:
            soma = 0
            prob.append(i)
            rmae.append(mae['MAE'][i] / self.reference[i])

        rmae_serie = pd.Series(rmae, index=prob, name='RMAE')
        return rmae_serie
