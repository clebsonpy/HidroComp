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
                                  type_threshold='stationary',
                                  type_event='cheia',
                                  value_threshold=0.75,
                                  type_criterion='xmin_maior_dois_terco_x',
                                  duration=0)

    name = "SDP 9"
    print(len(parcial1.event_peaks()))
    print(parcial1.mvs())
    parcial1.plot_hydrogram(name, save=True)
    #parcial1.plot_distribution(title=name, type_function='cumulative')
    #parcial1.plot_distribution(title=name, type_function='density')

    #print(maximum.mml())
    #print(maximum.peaks)
    #maximum.plot_hydrogram()
    #maximum.plot_distribution(title='maxima', type_function='cumulative', estimador='mml')
    #maximum.plot_distribution(title='maxima', type_function='density', estimador='mml')

    #print(plot)

    #Comparation_Distribution([plot]).plot()

    fim = timeit.default_timer()
    print('Duração: ', fim-ini)
