"""
Created on 21 de mar de 2018

@author: clebson
"""
import os

from files.fileRead import FileRead


class Cemaden(FileRead):
    """
    class files read: Centro Nacional de Monitoramento e
                    Alertas de Desastres Naturais - CEMADEN
    """
    font = 'Cemaden'
    extension = 'sam'
    def __init__(self, path=os.getcwd()):
        super().__init__(path)

    def list_files(self):
        super().list_files()

    def read(self, name=None):
        if name is None:
            return super().read()
        else:
            self.name = name
            data = self.__read_sam()
            return data

    def __lines_sam(self):
        list_lines = []
        with open(os.path.join(self.path, self.name+'.'+Cemaden.extension), 'r') as arq:
            for line in arq.readlines():
                list_lines.append(line.split())
        return list_lines

    def __read_sam(self):
        list_lines = self.__lines_sam()
        dic = {'dado': [], 'columns': []}
        cont = 0
        for line in list_lines:
            if cont > 0:
                dataHora = pd.to_datetime(self.name)
                dic['dado'].append(float(line[3]))
                dic['columns'].append((line[1], line[2]))
            cont +=1
        pf = pd.DataFrame(dic, index=dataHora, columns=dic['columns'])
        return pd
