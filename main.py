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
    """
    parcial = serie_vazao.parcial(station='XINGO',
                                  type_threshold='events_by_year',
                                  type_event='cheia',
                                  value_threshold=2.3,
                                  type_criterion='autocorrelação',
                                  duration=0)

    parcial1 = serie_vazao.parcial(station='XINGO',
                                  type_threshold='stationary',
                                  type_event='cheia',
                                  value_threshold=0.75,
                                  type_criterion='mediana',
                                  duration=0)

    parcial2 = serie_vazao.parcial(station='XINGO',
                                  type_threshold='stationary',
                                  type_event='cheia',
                                  value_threshold=0.75,
                                  type_criterion='xmin_maior_qmin',
                                  duration=0)

    parcial3 = serie_vazao.parcial(station='XINGO',
                                  type_threshold='stationary',
                                  type_event='cheia',
                                  value_threshold=0.75,
                                  type_criterion='xmin_maior_dois_terco_x',
                                  duration=0)

    name = "Referencia"
    #print(len(parcial1.event_peaks()))
    #print(parcial1.mvs())
    #print(parcial1.peaks)
    #parcial1.plot_hydrogram(name, save=True)
    data, fig = parcial.plot_distribution(title=name, type_function='density', save=True)
    #parcial1.plot_distribution(title=name, type_function='density')

    name = "SDP 7"
    data1, fig1 = parcial1.plot_distribution(title=name, type_function='density', save=True)
    data1.line['dash'] = 'dot'

    name = "SDP 8"
    data2, fig2 = parcial2.plot_distribution(title=name, type_function='density', save=True)
    data2.line['dash'] = 'dash'

    name = "SDP 9"
    data3, fig3 = parcial3.plot_distribution(title=name, type_function='density', save=True)
    data3.line['dash'] = 'dashdot'
    """
    print(maximum.mml())
    print(maximum.peaks)
    maximum.plot_hydrogram()
    maximum.plot_distribution(title='Máximas Anuais', type_function='cumulative', estimador='mml')
    maximum.plot_distribution(title='Máximas Anuais', type_function='density', estimador='mml')

    #print(plot)

    #Comparation_Distribution([data]).plot()

    fim = timeit.default_timer()
    print('Duração: ', fim-ini)
