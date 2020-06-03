"""
Created on 21 de mar de 2018

@author: clebson
"""

import os
import calendar as ca

import numpy as np
import pandas as pd
from hidrocomp.files.fileRead import FileRead
from api_ana.serie_temporal import SerieTemporal


class Ana(FileRead):
    """
    class files read: Agência Nacinal de Águas - ANA
    """
    typesData = {'FLUVIOMÉTRICO': ['Vazao{:02}', 'vazoes', '3'],
                 'PLUVIOMÉTRICO': ['Chuva{:02}', 'chuvas', '2'],
                 'COTA': ['Cota{:02}', 'cotas', '1']}
    source = "ANA"
    extension = "txt"

    def __init__(self, path_file=None, station=None, type_data='FLUVIOMÉTRICO', consistence='1', date_start='',
                 date_end='', *args, **kwargs):
        super().__init__(path_file=path_file, station=station, *args, **kwargs)
        self.consistence = consistence
        self.date_start = date_start
        self.date_end = date_end
        self.type_data = type_data.upper()
        self.data = self.read(self.name)
        try:
            self.mean = kwargs["mean"]
        except KeyError:
            self.mean = None

    def list_files(self):
        return super().list_files()

    def read(self, name=None):
        if self.api:
            if name is None:
                self.name = self.path
                return super().read()
            else:
                self.name = name
                data = self.__excludes_duplicates(self.hidro_serie_historica())
        else:
            if name is None or name is not list:
                self.name = self.list_files()
                return super().read()
            else:
                self.name = name
                data = self.__excludes_duplicates(self.__readTxt())
        return data

    def __lines(self):
        list_lines = []
        with open(os.path.join(self.path, self.name + '.' + Ana.extension),
                  encoding="Latin-1") as file:
            l = 0
            for line in file.readlines():
                if line.split(";")[0] == "EstacaoCodigo":
                    l = 1
                    list_lines.append(line.split(";"))
                elif l == 1:
                    list_lines.append(line.split(";"))

        return list_lines

    def __multIndex(self, date, days, consistence):
        if date.day == 1:
            n_days = days
        else:
            n_days = days - date.day
        list_date = pd.date_range(date, periods=n_days, freq="D")
        list_cons = [int(consistence)] * n_days
        index_multi = list(zip(*[list_date, list_cons]))
        return pd.MultiIndex.from_tuples(index_multi, names=["Date", "Consistence"])

    def __readTxt(self):
        list_lines = self.__lines()
        data_flow = list()
        count = 0
        for line in list_lines:
            count += 1
            if count == 1:
                idx_code = line.index("EstacaoCodigo")
                start_flow = line.index(Ana.typesData[self.type_data][0].format(1))
                idx_date = line.index("Data")
                idx_cons = line.index("NivelConsistencia")
            elif count >= 2:
                code = line[idx_code]
                date = pd.to_datetime(line[idx_date], dayfirst=True)
                days = ca.monthrange(date.year, date.month)[1]
                consistence = line[idx_cons]
                index = self.__multIndex(date, days, consistence)
                idx_flow = [i for i in range(start_flow, start_flow + days)]
                list_flow = [np.NaN if line[i] == "" else float(
                    line[i].replace(",", ".")) for i in idx_flow]
                data_flow.append(
                    pd.Series(list_flow, index=index, name="{}_{}".format(code, self.type_data[:3])))
        data_flow = pd.DataFrame(pd.concat(data_flow))
        return data_flow

    def hidro_serie_historica(self):
        serie_temporal = SerieTemporal()
        data = serie_temporal.get(codEstacao=self.name, dataInicio=self.date_start, dataFim=self.date_end,
                                  tipoDados=Ana.typesData[self.type_data][2], nivelConsistencia=self.consistence)
        return data

    def __excludes_duplicates(self, data):
        if len(data) > 0:
            if self.consistence == '1':  # bruto_e_consistido
                ordem = data.copy(deep=True)
                eh_duplicata = ordem.reset_index(level=1, drop=True).index.duplicated(keep='last')
                saida = data[~eh_duplicata]
            elif self.consistence == '2':  # somente consistidos
                try:
                    saida = data.iloc[data.index.isin([self.consistence], level=1)]
                except KeyError:
                    return
        else:
            return data
        return saida.reset_index(level=1, drop=True).groupby(pd.Grouper(freq='D')).mean()
