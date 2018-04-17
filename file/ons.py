'''
Created on 21 de ago de 2017

@author: clebson
'''
from fileRead import FileRead
import os
import pandas as pd
import numpy as np

class Ons(FileRead):

    font = "ONS"
    extension = "xls"
    def __init__(self, path = os.getcwd()):
        super().__init__(path)
        self.datas = self.read(self.name)

    def listFiles(self):
        return super().list_files()

    def read(self, name = None):
        if name == None:
            return super().read()
        else:
            self.name = name
            return self.__readLxs()

    def __readLxs(self):
        fileOns = os.path.join(self.path, self.name+'.xls')
        dataFlow = pd.read_excel(fileOns, shettname='Total', header=0, skiprows=5, index_col=0)
        dataFlow.drop(np.NaN, inplace=True)
        
        aux = []
        dic = {'jan':'1', 'fev':'2', 'mar':'3', 'abr':'4', 'mai':'5', 'jun':'6', 'jul':'7', 'ago':'8', 'set':'9', 'out':'10', 'nov':'11', 'dez':'12'}
        for i in dataFlow.index:
            aux.append(i.replace(i[-8:-5], dic[i[-8:-5]]))

        dataFlow.index = pd.to_datetime(aux, dayfirst=True)
        codeColumn = [i.split(' (')[0] for i in dataFlow.axes[1]]
        dataFlow.columns = codeColumn

        return dataFlow.astype(float)