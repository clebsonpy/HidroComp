"""
Created on 21 de mar de 2018

@author: clebson
"""

import os
import multiprocessing as mp
import pandas as pd
from file.files import Files
from abc import abstractmethod, ABCMeta


class FileRead(Files):
    
    __metaclass__ = ABCMeta

    def __init__(self, path=os.getcwd(), type_data='FLUVIOMÉTRICO'):
        if os.path.isfile(path):
            self.path = os.path.dirname(path)
            self.name, ext = os.path.splitext(os.path.basename(path))
            if ext != self.extension:
                raise Exception('Formato invalido')
        elif os.path.isdir(path):
            self.path = path
            self.name = None
        else:
            raise Exception('Arquivo ou diretório não existe')
        super().__init__(path)
        
    @abstractmethod
    def list_files(self):
        return super().list_files()
    
    @abstractmethod
    def read(self):
        self.name = self.list_files()
        if type(self.name) == list:
            p = mp.Pool(4)
            listaDfs = p.map(self.read, self.name)
            p.close()
            dataFlow = pd.DataFrame()
            for df in listaDfs:
                dataFlow = dataFlow.combine_first(df)
            return dataFlow.sort_index()
        else:
            return self.read(self.name)