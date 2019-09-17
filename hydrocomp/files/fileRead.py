"""
Created on 21 de mar de 2018

@author: clebson
"""
import os
import multiprocessing as mp
import pandas as pd
from hydrocomp.files.files import Files
from abc import abstractmethod, ABCMeta


class FileRead(Files, metaclass=ABCMeta):

    def __init__(self, path=os.getcwd()):
        if os.path.isfile(path):
            self.path = os.path.dirname(path)
            self.name, ext = os.path.splitext(os.path.basename(path))
            if ext != ".{}".format(self.extension):
                raise Exception('Formato invalido')
        elif os.path.isdir(path):
            self.path = path
            self.name = None
        else:
            raise Exception('Arquivo ou diretório não existe')
        super().__init__(self.path)

    @abstractmethod
    def list_files(self):
        return super().list_files()

    @abstractmethod
    def read(self):
        self.name = self.list_files()
        if type(self.name) == list and len(self.name) > 1:
            p = mp.Pool(4)
            listaDfs = p.map(self.read, self.name)
            p.close()
            if self.source == 'ANA':
                dataFlow = pd.DataFrame()
                for df in listaDfs:
                    dataFlow = dataFlow.combine_first(df)
                return dataFlow.sort_index()
            else:
                dataFlow = pd.DataFrame(listaDfs)
                return dataFlow.sort_index()
        else:
            return self.read(self.name)
