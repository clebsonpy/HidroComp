import pandas as pd

from comparasion.quantify_uncertainty import QuantifyUncertainty


class MAE(QuantifyUncertainty):
    """
    Mean Absolute Error - RMSE
    MAE = [1/n * soma|(xi - Qmax)|]
    """
    def __init__(self, reference, compared):
        """Dados de entrada:
            reference: <pd.DataFrame> com as magnitudes estimadas pela distribuiçao
            de referência.
            compared: <dict> contendo os <pd.DataFrame> com as magnitudes estimadas
            pelas distribuições a serem comparadas.
        """
        super().__init__(reference, compared)

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
