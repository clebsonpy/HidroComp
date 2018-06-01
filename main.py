import pandas as pd

from files.cemaden import Cemaden
from files.fileWrite import FileWrite

import timeit

if __name__ == '__main__':
    ini = timeit.default_timer()
    path = "/home/clebson/Documentos/Projetos/201409_output_10minutos"
    dados = Cemaden(path).read()
    FileWrite(dados).txt(name_dir='output', hour=False)

    fim = timeit.default_timer()
    print('Duração: ', fim-ini)
