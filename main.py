from series.vazao import Vazao
import timeit

if __name__ == '__main__':
    ini = timeit.default_timer()
    path = "/home/clebson/Documentos/Projetos/HidroComp1_8"
    serie_vazao = Vazao(path=path, font='ONS')
    serie_vazao.date(date_start='1/1/1999')
    parcial = serie_vazao.parcial(station='XINGO',
                                  type_threshold='stationary',
                                  type_event='cheia',
                                  value_threshold=0.75,
                                  type_criterion='media')

    print(parcial.event_peaks(duration=5))

    fim = timeit.default_timer()
    print('Duração: ', fim-ini)
