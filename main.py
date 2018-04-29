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
                                  type_threshold='events_by_year',
                                  type_event='cheia',
                                  value_threshold=1.65,
                                  type_criterion='xmin_maior_dois_terco',
                                  duration=0)

    print(parcial.event_peaks())
    print(len(parcial.peaks))
    print(parcial.plot_hydrogram('Test'))


    #print(plot)

    #Comparation_Distribution([plot]).plot()

    fim = timeit.default_timer()
    print('Duração: ', fim-ini)
