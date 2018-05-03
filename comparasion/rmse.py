import pandas as pd

from comparasion.quantify_uncertainty import QuantifyUncertainty


class RMSE(QuantifyUncertainty):
    """
    Root Mean Square Error - RMSE
    RMSE = [1/n * soma(xi - Qmax)²]^1/2
    """
    def __init__(self, reference, compared):
        super().__init__(reference, compared)

    def calculo_erro(self, compared):
        rmse = []
        prob = []
        soma = 0
        for i in self.reference.index:
            prob.append(i)
            aux = (compared[i] - self.reference[i]) ** 2
            soma += aux

            rmse.append(aux ** 0.5)

        rmse_value = (1/len(compared)*soma) ** 0.5
        rmse.append(rmse_value)
        prob.append('RMSE')
        rmse_serie = pd.Series(rmse, index=prob, name=compared.name)
        return rmse_serie
