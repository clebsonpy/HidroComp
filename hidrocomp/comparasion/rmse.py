import pandas as pd

from hidrocomp.comparasion.quantify_uncertainty import QuantifyUncertainty


class RMSE(QuantifyUncertainty):
    """
    Root Mean Square Error - RMSE
    RMSE = [1/n * soma(xi - Qmax)²]^1/2
    """
    def __init__(self, reference, compared):
        super().__init__(reference, compared)

    def calculo_erro(self):
        prob = list()
        rmse = list()
        for i in self.reference.index:
            sum = 0
            prob.append(i)
            for j in self.compared[i].values:
                aux = (j - self.reference[i]) ** 2
                sum += aux

            rmse_value = (1/len(self.compared)*sum) ** 0.5
            rmse.append(rmse_value)

        rmse_serie = pd.Series(rmse, index=prob, name='RMSE')
        return rmse_serie
