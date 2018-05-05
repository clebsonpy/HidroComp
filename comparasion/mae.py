import pandas as pd

from comparasion.quantify_uncertainty import QuantifyUncertainty


class MAE(QuantifyUncertainty):
    """
    Mean Absolute Error - RMSE
    MAE = [1/n * soma|(xi - Qmax)|]
    """
    def __init__(self, reference, compared):
        super().__init__(reference, compared)

    def calculo_erro(self):
        prob = []
        mae = []
        for i in self.reference.index:
            soma = 0
            prob.append(i)
            for j in self.compared[i].values:
                aux = abs(j - self.reference[i])
                soma += aux

            mae_value = ((1/len(self.compared))*soma)
            mae.append(mae_value)

        mae_serie = pd.Series(mae, index=prob, name='MAE')
        return mae_serie
