"""
Created on 21 de mar de 2018

@author: clebson
"""
import os
import pandas as pd

from hidrocomp.files.fileRead import FileRead


class Cemaden(FileRead):
    """
    class files read: Centro Nacional de Monitoramento e
                    Alertas de Desastres Naturais - CEMADEN
    """
    source = 'Cemaden'
    extension = 'sam'

    def __init__(self, path_file=os.getcwd()):
        super().__init__(path_file)

    def list_files(self):
        pass

    def read(self, name=None):
        if name is None:
            return super().read()
        else:
            self.name = name
            data = self.__read_sam()
            return data

    def __lines_sam(self):
        list_lines = []
        with open(os.path.join(self.path, self.name+'.'+Cemaden.extension), 'r') as \
                arq:
            for line in arq.readlines():
                list_lines.append(line.split())
        return list_lines

    def __read_sam(self):
        list_lines = self.__lines_sam()
        dado = []
        index = []
        data = self.name.split('_')[1].replace('-', '')
        date_hour = pd.to_datetime(data)
        cont = 0
        for line in list_lines:
            if cont > 0:
                dado.append(float(line[3]))
                index.append((line[1], line[2]))
            cont += 1
        se = pd.Series(dado, index=index, name=date_hour)
        return se
