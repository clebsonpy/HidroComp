"""
Created on 21 de mar de 2018

@author: clebson
"""

import os
from abc import ABCMeta, abstractmethod


class Files(object):

    __metaclass__ = ABCMeta

    def __init__(self, path=os.getcwd()):
        self.path = path
    
    @abstractmethod
    def list_files(self):
        listaDir = os.listdir(self.path)
        listFile = []
        for file in listaDir:
            if os.path.isfile(os.path.join(self.path, file)):
                if file.lower().endswith(self.extension.lower()):            
                    name, ext = os.path.splitext(file)
                    listFile.append(name)
        if len(listFile) == 1:
            listFile = listFile[0]
        return listFile
