"""
Created on 21 de mar de 2018

@author: clebson
"""
import pandas as pd
import os

from hidrocomp.files import Files


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

    def txt(self, name_dir, hour=True):
        if hour:
            pass
        else:
            self.df = self.df.resample('H').sum()
        bool = self.df.isnull()
        cont = 1
        arq2 = open(os.path.join(os.getcwd(), 'interplu'+'.txt'), 'w')
        arq2.write('{:>20}{:>23}{:>13}\n'.format('codigo', 'long dec', 'lat dec'))
        for i in self.df:
            data = pd.to_datetime('1/1/1977')
            name_arq = '{:08}.txt'.format(cont)
            cont += 1
            arq2.write('{:>20}{:>23}{:>13}\n'.format(name_arq, i[0], i[1]))
            arq = open(os.path.join(os.path.join(os.getcwd(),
                                                 name_dir), name_arq), 'w')
            for j in self.df[i].index:
                if bool[i][j]:
                    j =- 1
                else:
                    j = self.df[i][j]
                arq.write('{:>6}{:>6}{:>6}{:>12}\n'.format(data.day, data.month,
                                                           data.year, j))
                data += pd.DateOffset(days=1)
            arq.close()
        arq2.close()
