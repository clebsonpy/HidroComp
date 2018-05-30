"""
Created on 21 de mar de 2018

@author: clebson
"""
import pandas as pd
import os

from files.files import Files


class FileWrite(Files):

    def __init__(self, df, name=None):
        self.df = df
        self.name = name

    def excel(self):
        writer = pd.ExcelWriter('%s.xlsx' % self.name)
        self.df.to_excel(writer)
        writer.save()

    def csv(self):
        self.df.to_csv('%s.csv' % self.name)

    def json(self):
        self.df.to_json('%s.json' % self.name)

    def txt(self, name_dir):
        bool = self.df.isnull()
        for i in self.df:
            data = pd.to_datetime('1/1/1977')
            name_arq = 'log_%s-lat_%s' % i
            name_arq = name_arq.replace('.','_')
            arq = open(os.path.join(os.path.join(os.getcwd(),name_dir), name_arq+'.txt'), 'w')
            for j in self.df[i].index:
                if bool[i][j]:
                    j=-1
                else:
                    j=self.df[i][j]
                arq.write('{:>6}{:>6}{:>6}{:>12}\n'.format(data.day, data.month,
                                                           data.year, j))
                data+=pd.DateOffset(days=1)
            arq.close()
