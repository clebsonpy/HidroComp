"""
Created on 21 de mar de 2018

@author: clebson
"""

import os
from abc import ABCMeta
import calendar as ca
import numpy as np
import pandas as pd
from file.fileRead import FileRead


class Ana(FileRead):
    """
    class files read: Agência Nacinal de Águas - ANA
    """

    ___metaclass__ = ABCMeta

    typesData = {'FLUVIOMÉTRICO': 'Vazao01',
                 'PLUVIOMÉTRICO': 'Chuva01'}
    font = "ANA"
    extension = "TXT"

    def __init__(self, path=os.getcwd(), type_data='FLUVIOMÉTRICO', consistencia=2):
        super().__init__(path)
        self.consistencia = consistencia
        self.type_data = type_data.upper()
        self.data = self.read(self.name)

    def list_files(self):
        return super().list_files()

    def read(self, name=None):
        if name is None:
            return super().read()
        else:
            self.name = name
            data = self.__readTxt()
            data = data.iloc[data.index.isin([self.consistencia], level=1)]
            data.reset_index(level=1, drop=True, inplace=True)
            return data
    
    def __lines(self):
        list_lines = []
        with open(os.path.join(self.path, self.name+'.'+Ana.extension), encoding="Latin-1") as file:
            for line in file.readlines():
                if line[:3] != "// " and line[:3] != "//-" and line != "\n" and line !="//\n":
                    list_lines.append(line.strip("//").split(";"))
        return list_lines

    def __multIndex(self, date, days, consistencia):
        if date.day == 1:
            n_days = days
        else:
            n_days = days - date.day
        list_date = pd.date_range(date, periods=n_days, freq="D")
        list_cons = [int(consistencia)]*n_days
        index_mult = list(zip(*[list_date, list_cons]))
        return pd.MultiIndex.from_tuples(index_mult, names=["Data", "Consistencia"])
    
    def __readTxt(self):
        list_lines = self.__lines()
        data_flow = []
        count = 0
        for line in list_lines:
            count += 1
            if count == 1:
                idx_code = line.index("EstacaoCodigo")
                start_flow = line.index(Ana.typesData[self.type_data])
                idx_date = line.index("Data")
                idx_cons = line.index("NivelConsistencia")
            elif count >= 2:
                code = line[idx_code]
                date = pd.to_datetime(line[idx_date], dayfirst=True)
                days = ca.monthrange(date.year, date.month)[1]
                consistencia = line[idx_cons]
                index = self.__multIndex(date, days, consistencia)
                idx_flow = [i for i in range(start_flow, start_flow + days)]
                list_flow = [np.NaN if line[i] == "" else float(
                    line[i].replace(",", ".")) for i in idx_flow]
                data_flow.append(
                    pd.Series(list_flow, index=index, name=code))
        data_flow = pd.DataFrame(pd.concat(data_flow))
        return data_flow
