"""
Created on 21 de mar de 2018

@author: clebson
"""

from hidrocomp.files.fileRead import FileRead
import os
import pandas as pd
import numpy as np


class Ons(FileRead):

    source = "ONS"
    extension = "xlsx"

    def __init__(self, path_file=None, type_data='FLUVIOMÉTRICO', station=None, *args, **kwargs):
        super().__init__(path_file)
        self.type_data = type_data
        self.station = station
        if self.station is None:
            self.data = self.read(self.station)
        else:
            self.data = pd.DataFrame(self.read(self.station)[self.station])
        self.inf_stations = None

    def list_files(self):
        return super().list_files()

    def read(self, name=None):
        if self.api:
            if name is None:
                self.name = ""
                return super().read()
            else:
                self.name = name
                return self.__series_temporal()
        else:
            if name is None:
                return super().read()
            else:
                self.name = name
                return self.__read_xls()

    def __read_xls(self):
        file_ons = os.path.join(self.path, self.name+'.'+Ons.extension)
        data_flow = pd.read_excel(file_ons, shettname='Total', header=0, skiprows=5, index_col=0)
        data_flow.drop(np.NaN, inplace=True)

        aux = []
        dic = {'jan': '1', 'fev': '2', 'mar': '3', 'abr': '4', 'mai': '5',
               'jun': '6', 'jul': '7', 'ago': '8', 'set': '9', 'out': '10',
               'nov': '11', 'dez': '12'
               }
        for i in data_flow.index:
            aux.append(i.replace(i[-8:-5], dic[i[-8:-5]]))

        data_flow.index = pd.to_datetime(aux, dayfirst=True)
        code_column = [i.split(' (')[0] for i in data_flow.axes[1]]
        data_flow.columns = code_column

        return data_flow.astype(float)

    def __series_temporal(self):
        data = pd.read_csv('http://raw.githubusercontent.com/wallissoncarvalho/hydrobr/master/hydrobr/'
                           'resources/ONS_daily_flow.csv', index_col=0, parse_dates=True)
        code_column = [i.split(' (')[0] for i in data.axes[1]]
        data.columns = code_column
        data.index.name = None
        return data

