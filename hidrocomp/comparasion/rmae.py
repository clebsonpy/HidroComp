import pandas as pd

from hidrocomp.comparasion.mae import MAE
from hidrocomp.comparasion.quantify_uncertainty import QuantifyUncertainty


class RMAE(QuantifyUncertainty):
    """
    Relative Mean Absolute Error - RMSE
    RMAE = MAE/mean(Qmax)
    """
    def __init__(self, reference, compared):
        super().__init__(reference, compared)

    def calculo_erro(self):
        mae = MAE(self.reference, self.compared).quantify()
        prob = list()
        rmae = list()
        for i in self.reference.index:
            prob.append(i)
            rmae.append(mae['MAE'][i] / self.reference[i])

        rmae_serie = pd.Series(rmae, index=prob, name='RMAE')
        return rmae_serie
