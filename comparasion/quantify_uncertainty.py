import pandas as pd

from abc import ABCMeta, abstractmethod


class QuantifyUncertainty(object, metaclass=ABCMeta):

    def __init__(self, reference, compared):
        self.reference = reference
        self.compared = compared

    def quantify(self):
        df_comp = pd.DataFrame()
        for i in self.compared:
            df = self.__rmse(self.compared[i], i)
            df_comp = df_comp.combine_first(df)
        return df_comp
