import pandas as pd

from files.cemaden import Cemaden
from series.vazao import Vazao
from comparasion.rmse import RMSE
from comparasion.mae import MAE
from comparasion.rmae import RMAE

from graphics.comparation_distribution import Comparation_Distribution
from graphics.boxplot import Boxplot
import timeit

if __name__ == '__main__':
    ini = timeit.default_timer()
    path = "/home/clebson/Documentos/Projetos/201405_output_horário"
    dados = Cemaden(path)
    print(dados.read())
    #dados = pd.read_csv("dadosXingo.csv", index_col=0, names=[
    #                    "Data", "XINGO"], parse_dates=True)
    #serie_vazao = Vazao(data=dados, path=path, font='ONS')
    #serie_vazao.date(date_start='1/1/1999')
    #print(serie_vazao.plot_hydrogram('XINGO'))

    fim = timeit.default_timer()
    print('Duração: ', fim-ini)
