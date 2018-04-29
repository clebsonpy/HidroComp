import pandas as pd
import numpy as np

from comparasion.quantify_uncertainty import QuantifyUncertainty


class RMSE(QuantifyUncertainty):
    """
    Root Mean Square Error - RMSE
    RMSE = [1/n * soma(xi - Qmax)²]^1/2
    """
    def __init__(self, reference, compared):
        super().__init__(reference, compared)

    def resample_quantify(self):
        pass

    def __rmse(self, compared=None, type_criterion=None):
        rmse = []
        prob = []
        for i in self.reference:
            soma = 0
            prob.append(i)
            for x in compared[i]:
                aux = (x - self.reference[i].values[0])
                soma += np.power(aux, 2)

            aux2 = (1/len(compared))*soma
            rmse.append(np.power(aux2, 0.5))
        name = ('RMSE', type_criterion)
        return pd.DataFrame(rmse, index=prob, columns=[name])

    def quantify(self):
        df_rmse = pd.DataFrame()
        for i in self.compared:
            df = self.__rmse(self.compared[i], i)
            df_rmse = df_rmse.combine_first(df)
        return df_rmse
