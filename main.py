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

    parcial1 = serie_vazao.parcial(station='XINGO',
                                  type_threshold='stationary',
                                  type_event='cheia',
                                  value_threshold=0.75,
                                  type_criterion='autocorrelação',
                                  duration=0)

    parcial2 = serie_vazao.parcial(station='XINGO',
                                  type_threshold='stationary',
                                  type_event='cheia',
                                  value_threshold=0.75,
                                  type_criterion='media',
                                  duration=0)

    compared = parcial2.magnitudes()
    reference = parcial1.magnitudes()

    rmse = parcial1.rmse(compared)
    print(rmse)
    #print(parcial.event_peaks())
    #print(parcial.resample(tamanho=25, quantidade=100))

    #print(plot)

    #Comparation_Distribution([plot]).plot()

    fim = timeit.default_timer()
    print('Duração: ', fim-ini)
