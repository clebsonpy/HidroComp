"""
Created on 21 de mar de 2018

@author: clebson
"""

import os
from abc import ABCMeta, abstractmethod


class Files(metaclass=ABCMeta):

    def __init__(self, path_file=None):
        self.path = path_file

    @abstractmethod
    def list_files(self):
        list_dir = os.listdir(self.path)
        list_file = list()
        for file in list_dir:
            if os.path.isfile(os.path.join(self.path, file)):
                if file.lower().endswith(self.extension.lower()):
                    name, ext = os.path.splitext(file)
                    if self.source == "ONS":
                        list_file.append(name)
                    elif self.source == "ANA":
                        if name.split("_T_")[0] == self.typesData[self.type_data][1]:
                            list_file.append(name)
        if len(list_file) == 1:
            list_file = list_file[0]
        return list_file
