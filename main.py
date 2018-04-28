from series.vazao import Vazao
from graphics.comparation_distribution import Comparation_Distribution
import timeit

if __name__ == '__main__':
    ini = timeit.default_timer()
    path = "/home/clebson/Documentos/Projetos/HidroComp1_8"
    serie_vazao = Vazao(path=path, font='ONS')
    serie_vazao.date(date_start='1/1/1999')
    #print(serie_vazao.plot_hydrogram('XINGO'))

    #maximum = serie_vazao.maximum(station='XINGO')

    parcial = serie_vazao.parcial(station='XINGO',
                                  type_threshold='stationary',
                                  type_event='cheia',
                                  value_threshold=0.75,
                                  type_criterion='autocorrelação',
                                  duration=0)
    plot = parcial.plot_distribution('Ref', 'cumulative')

    parcial1 = serie_vazao.parcial(station='XINGO',
                                  type_threshold='stationary',
                                  type_event='cheia',
                                  value_threshold=0.75,
                                  type_criterion='media',
                                  duration=0)


    plot1 = parcial1.plot_distribution('media', 'cumulative')

    print(plot, plot1)

    Comparation_Distribution([plot, plot1]).plot()

    fim = timeit.default_timer()
    print('Duração: ', fim-ini)
