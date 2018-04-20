"""
Created on 21 de mar de 2018

@author: clebson
"""

from ons import Ons
import timeit

if __name__ == '__main__':
    start = timeit.default_timer()
    path = "/home/clebson/Documentos/Projetos/HidroComp1_8"
    obAna = Ons(path)
    print(obAna.data.XINGO)
    end = timeit.default_timer()
    print('Duração: %s' % (end - start))
