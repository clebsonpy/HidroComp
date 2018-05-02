from series.vazao import Vazao
from comparasion.rmse import RMSE
from comparasion.mae import MAE
from comparasion.rmae import RMAE

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
                                  type_threshold='autocorrelação',
                                  type_event='cheia',
                                  value_threshold=0,
                                  type_criterion='autocorrelação',
                                  duration=1)
    """
    parcial2 = serie_vazao.parcial(station='XINGO',
                                  type_threshold='stationary',
                                  type_event='cheia',
                                  value_threshold=0.75,
                                  type_criterion='media',
                                  duration=0)

    parcial3 = serie_vazao.parcial(station='XINGO',
                                  type_threshold='stationary',
                                  type_event='cheia',
                                  value_threshold=0.75,
                                  type_criterion='mediana',
                                  duration=0)

    parcial4 = serie_vazao.parcial(station='XINGO',
                                  type_threshold='events_by_year',
                                  type_event='cheia',
                                  value_threshold=1.65,
                                  type_criterion='media',
                                  duration=0)


    reference = parcial1.magnitude(tempos_retorno)
    compared2 = parcial2.magnitude(tempos_retorno)
    compared3 = parcial3.magnitude(tempos_retorno)
    #compared4 = parcial4.magnitude(tempos_retorno)

    rmse = RMSE(reference, [compared2, compared3])
    mae = MAE(reference, [compared2, compared3])
    rmae = RMAE(reference, [compared2, compared3])
    print(rmse.quantify())
    print(mae.quantify())
    print(rmae.quantify())

    tempos_retorno = [2, 5, 10, 25, 50, 100, 500]
    #print(parcial1.event_peaks())

    reference = parcial1.magnitude(tempos_retorno)
    compared2 = parcial1.magnitude_resample(quantidade=150, tempo_de_retorno=tempos_retorno)
    rmse = RMSE(reference, compared2)
    mae = MAE(reference, compared2)
    rmae = RMAE(reference, compared2)
    print(rmse.quantify_resample())
    print(mae.quantify_resample())
    print(rmae.quantify_resample())
    """
    parcial1.plot_hydrogram('autocorrelacao')

    fim = timeit.default_timer()
    print('Duração: ', fim-ini)
