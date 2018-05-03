import pandas as pd

from series.vazao import Vazao
from comparasion.rmse import RMSE
from comparasion.mae import MAE
from comparasion.rmae import RMAE

from graphics.comparation_distribution import Comparation_Distribution
import timeit

if __name__ == '__main__':
    ini = timeit.default_timer()
    path = "/home/clebson/Documentos/Projetos/HidroComp1_8"
    dados = pd.read_csv("dadosXingo.csv", index_col=0, names=[
                        "Data", "XINGO"], parse_dates=True)
    serie_vazao = Vazao(data=dados, path=path, font='ONS')
    serie_vazao.date(date_start='1/1/1999')
    #print(serie_vazao.plot_hydrogram('XINGO'))

    maximum = serie_vazao.maximum(station='XINGO')

    parcial1 = serie_vazao.parcial(station='XINGO',
                                  type_threshold='events_by_year',
                                  type_event='cheia',
                                  value_threshold=2.3,
                                  type_criterion='autocorrelação',
                                  duration=0)

    print(parcial1.mvs())
    parcial1.plot_hydrogram("Referência")
    parcial1.plot_distribution(title="Referência", type_function='cumulative')
    parcial1.plot_distribution(title="Referência", type_function='density')

    #print(maximum.mvs())
    #maximum.plot_hydrogram()
    #maximum.plot_distribution(title='maxima', type_function='cumulative')
    #maximum.plot_distribution(title='maxima', type_function='density')

    #print(plot)

    #Comparation_Distribution([plot]).plot()

    fim = timeit.default_timer()
    print('Duração: ', fim-ini)
