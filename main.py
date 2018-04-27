from series.vazao import Vazao
import timeit

if __name__ == '__main__':
    ini = timeit.default_timer()
    path = "/home/clebson/Documentos/Projetos/HidroComp1_8"
    serie_vazao = Vazao(path=path, font='ONS')
    serie_vazao.date(date_start='1/1/1999')
    #maximum = serie_vazao.maximum(station='XINGO')

    parcial = serie_vazao.parcial(station='XINGO',
                                  type_threshold='stationary',
                                  type_event='cheia',
                                  value_threshold=0.75,
                                  type_criterion='autocorrelação',
                                  duration=5)

    #para_maximum = maximum.mvs()
    #para_parcial = parcial.mvs()
    print(parcial.plot_distribution('Test', 'cumulative'))
    #print(para_maximum)

    fim = timeit.default_timer()
    print('Duração: ', fim-ini)
