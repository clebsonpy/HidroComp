import pandas as pd

from comparasion.quantify_uncertainty import QuantifyUncertainty


class MAE(QuantifyUncertainty):
    """
    Mean Absolute Error - MAE
    MAE = [1/n * soma|(xi - Qmax)|]
    """
    name = 'MAE'
    def __init__(self, reference, compared):
        super().__init__(reference, compared, self.name)

    def formula(self, reference, compared):
        soma = 0
        for i in compared:
            soma += abs(i - reference)

        n = len(compared)
        return (1/n) * soma

    def calculo_erro(self, compared):
        mae = []
        prob = []
        soma = 0
        for i in self.reference.index:
            prob.append(i)
            aux = abs(compared[i] - self.reference[i])
            soma += aux

            mae.append(aux)

        mae_value = (1/len(compared)*soma)
        mae.append(mae_value)
        prob.append('MAE')
        mae_serie = pd.Series(mae, index=prob, name=compared.name)
        return mae_serie
