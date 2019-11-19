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

    def __init__(self, path_file=os.getcwd(), *args, **kwargs):
        try:
            if os.path.isfile(path_file):
                self.path = os.path.dirname(path_file)
                self.name, ext = os.path.splitext(os.path.basename(path_file))
                self.api = False
                if ext != ".{}".format(self.extension):
                    raise Exception('Formato invalido')
            elif os.path.isdir(path_file):
                self.path = path_file
                self.name = None
                self.api = False
            else:
                self.path = path_file
                self.name = None
                self.api = True
        except TypeError:
            self.path = path_file
            self.name = None
            self.api = True
        super().__init__(path_file=self.path)

    @abstractmethod
    def list_files(self):
        return super().list_files()

    @abstractmethod
    def read(self):
        if type(self.name) == list and len(self.name) > 1:
            p = mp.Pool(mp.cpu_count())
            listaDfs = p.map(self.read, self.name)
            p.close()
            if self.source == 'ANA':
                dataFlow = pd.DataFrame()
                for df in listaDfs:
                    if len(df) > 0:
                        dataFlow = dataFlow.combine_first(df)
                    else:
                        dataFlow = dataFlow
                return dataFlow.sort_index()
            else:
                dataFlow = pd.DataFrame(listaDfs)
                return dataFlow.sort_index()
        else:
            return self.read(self.name)
