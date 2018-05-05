import pandas as pd

from comparasion.quantify_uncertainty import QuantifyUncertainty


class RMSE(QuantifyUncertainty):
    """
    Root Mean Square Error - RMSE
    RMSE = [1/n * soma(xi - Qmax)²]^1/2
    """
    def __init__(self, reference, compared):
        super().__init__(reference, compared)

    def calculo_erro(self):
        prob = []
        rmse = []
        for i in self.reference.index:
            soma = 0
            prob.append(i)
            for j in self.compared[i].values:
                aux = (j - self.reference[i]) ** 2
                soma += aux

            rmse_value = (1/len(self.compared)*soma) ** 0.5
            rmse.append(rmse_value)

        rmse_serie = pd.Series(rmse, index=prob, name='RMSE')
        return rmse_serie
