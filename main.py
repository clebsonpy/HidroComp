import pandas as pd

from files.cemaden import Cemaden

import timeit

if __name__ == '__main__':
    ini = timeit.default_timer()
    path = "/home/clebson/Documentos/Projetos/201405_output_horário"
    dados = Cemaden(path)
    print(dados.read())

    fim = timeit.default_timer()
    print('Duração: ', fim-ini)
