"""
Created on 21 de mar de 2018

@author: clebson
"""

import os
import requests
import calendar as ca

import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
from hydrocomp.files.fileRead import FileRead


class Ana(FileRead):
    """
    class files read: Agência Nacinal de Águas - ANA
    """
    typesData = {'FLUVIOMÉTRICO': ['Vazao{:02}', 'vazoes', '3'],
                 'PLUVIOMÉTRICO': ['Chuva{:02}', 'chuvas', '2'],
                 'COTA': ['Cota{:02}', 'cotas', '1']}
    source = "ANA"
    extension = "txt"

    def __init__(self, path=os.getcwd(), type_data='FLUVIOMÉTRICO', consistence='', date_start='',
                 date_end='', *args, **kwargs):
        super().__init__(path, *args, **kwargs)
        self.consistence = consistence
        self.date_start = date_start
        self.date_end = date_end
        self.type_data = type_data.upper()
        if self.api:
            self.data = self.api_hidro_serie_historica()
        else:
            self.data = self.read(self.name)

    def list_files(self):
        return super().list_files()

    def read(self, name=None):
        if name is None:
            return super().read()
        else:
            self.name = name
            data = self.__readTxt()
            data = data.iloc[data.index.isin([self.consistence], level=1)]
            data.reset_index(level=1, drop=True, inplace=True)
            return data

    def __lines(self):
        list_lines = []
        with open(os.path.join(self.path, self.name+'.'+Ana.extension),
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

    def api_hidro_serie_historica(self):
        response = requests.get('http://telemetriaws1.ana.gov.br/ServiceANA.asmx/HidroSerieHistorica',
                                params={
                                    'codEstacao': self.name, 'dataInicio': self.date_start, 'dataFim': self.date_end,
                                    'tipoDados': Ana.typesData[self.type_data][2],
                                    'nivelConsistencia': self.consistence})

        tree = ET.ElementTree(ET.fromstring(response.content))
        root = tree.getroot()

        series = []
        for month in root.iter('SerieHistorica'):
            vazao = []
            codigo = month.find('EstacaoCodigo').text
            date_str = month.find('DataHora').text
            date = pd.to_datetime(date_str, dayfirst=True)
            days = ca.monthrange(date.year, date.month)[1]
            date_idx = pd.date_range(start=date_str, periods=days)
            for i in range(1, days + 1):
                value = Ana.typesData[self.type_data][0].format(i)
                try:
                    vazao.append(float(month.find(value).text))
                except TypeError:
                    vazao.append(month.find(value).text)
                except AttributeError:
                    vazao.append(None)
            series.append(pd.Series(vazao, index=date_idx, name=codigo))
        try:
            data_flow = pd.DataFrame(pd.concat(series))
        except ValueError:
            data_flow = pd.DataFrame(pd.Series(name=self.name))
        return data_flow
