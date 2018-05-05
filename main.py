import pandas as pd

from series.vazao import Vazao
from comparasion.rmse import RMSE
from comparasion.mae import MAE
from comparasion.rmae import RMAE

from graphics.comparation_distribution import Comparation_Distribution
from graphics.boxplot import Boxplot
import timeit

if __name__ == '__main__':
    ini = timeit.default_timer()
    path = "/home/clebson/Documentos/Projetos/HidroComp1_8"
    dados = pd.read_csv("dadosXingo.csv", index_col=0, names=[
                        "Data", "XINGO"], parse_dates=True)
    serie_vazao = Vazao(data=dados, path=path, font='ONS')
    serie_vazao.date(date_start='1/1/1999')
    #print(serie_vazao.plot_hydrogram('XINGO'))
    def pause():
    programPause = raw_input("Press the <ENTER> key to continue...")

    function = "density"
    def maximum(function):
        maximum = serie_vazao.maximum(station='XINGO')

        #print(maximum.mvs())
        #print(maximum.peaks)
        #maximum.plot_hydrogram()
        #maximum.plot_distribution(title='Máximas Anuais', type_function='cumulative', estimador='mml')
        data1, fig = maximum.plot_distribution(title='Máximas Anuais', type_function='density', estimador='mml')
        data1.line['dash'] = 'dashdot'
        data1.name = 'MML'
        data2, fig = maximum.plot_distribution(title='Máximas Anuais', type_function='density', estimador='mvs')
        data2.name = 'MVS'

    def referencia(function):
        parcial = serie_vazao.parcial(station='XINGO',
                                      type_threshold='events_by_year',
                                      type_event='cheia',
                                      value_threshold=2.3,
                                      type_criterion='autocorrelação',
                                      duration=0)


        name = "Referencia"
        #print(len(parcial.event_peaks()))
        #print(parcial.mvs())
        #print(parcial.peaks)
        #parcial.plot_hydrogram(name, save=True)
        #data, fig = parcial.plot_distribution(title=name, type_function=function, save=True)

    def sdp1(function, grafico, tempo_de_retorno):
        parcial1 = serie_vazao.parcial(station='XINGO',
                                      type_threshold='events_by_year',
                                      type_event='cheia',
                                      value_threshold=2.3,
                                      type_criterion='mediana',
                                      duration=0)

        name = "SDP 1"
        #print(len(parcial.event_peaks()))
        #print(parcial.mvs())
        #print(len(parcial.peaks))
        #print(parcial.peaks)
        if grafico == 'distribution':
            data, fig = parcial1.plot_distribution(title=name, type_function=function, save=True)
            data.line['dash'] = 'dot'
            return data, fig
        elif grafico == 'boxplot':
            data, fig = parcial1.plot_boxplot_resample(quantidade=100,
                                                      tempo_de_retorno=tempo_de_retorno,
                                                      save=True, name=name)
            return data, fig

    def sdp2(function, grafico, tempo_de_retorno):

        parcial2 = serie_vazao.parcial(station='XINGO',
                                      type_threshold='events_by_year',
                                      type_event='cheia',
                                      value_threshold=2.3,
                                      type_criterion='xmin_maior_qmin',
                                      duration=0)

        name = "SDP 2"
        if grafico == 'distribution':
            data, fig = parcial2.plot_distribution(title=name, type_function=function, save=True)
            data.line['dash'] = 'dash'
            return data, fig
        elif grafico == 'boxplot':
            data, fig = parcial2.plot_boxplot_resample(quantidade=100,
                                                      tempo_de_retorno=tempo_de_retorno,
                                                      save=True, name=name)
            return data, fig

    def sdp3(function, grafico, tempo_de_retorno):

        parcial3 = serie_vazao.parcial(station='XINGO',
                                      type_threshold='events_by_year',
                                      type_event='cheia',
                                      value_threshold=2.3,
                                      type_criterion='xmin_maior_dois_terco_x',
                                      duration=0)

        name = "SDP 3"
        if grafico == 'distribution':
            data, fig = parcial3.plot_distribution(title=name, type_function=function, save=True)
            data.line['dash'] = 'dashdot'
            return data, fig
        elif grafico == 'boxplot':
            data, fig = parcial3.plot_boxplot_resample(quantidade=100,
                                                      tempo_de_retorno=tempo_de_retorno,
                                                      save=True, name=name)
            return data, fig

    def sdp4(function, grafico, tempo_de_retorno):
        parcial4 = serie_vazao.parcial(station='XINGO',
                                      type_threshold='events_by_year',
                                      type_event='cheia',
                                      value_threshold=1.65,
                                      type_criterion='mediana',
                                      duration=0)


        name = "SDP 4"
        #print(len(parcial.event_peaks()))
        #print(parcial.mvs())
        #print(parcial.peaks)
        if grafico == 'distribution':
            data, fig = parcial4.plot_distribution(title=name, type_function=function, save=True)
            data.line['dash'] = 'dot'
            return data, fig
        elif grafico == 'boxplot':
            data, fig = parcial4.plot_boxplot_resample(quantidade=100,
                                                      tempo_de_retorno=tempo_de_retorno,
                                                      save=True, name=name)
            return data, fig

    def sdp5(function, grafico, tempo_de_retorno):

        parcial5 = serie_vazao.parcial(station='XINGO',
                                      type_threshold='events_by_year',
                                      type_event='cheia',
                                      value_threshold=1.65,
                                      type_criterion='xmin_maior_qmin',
                                      duration=0)

        name = "SDP 5"
        if grafico == 'distribution':
            data, fig = parcial5.plot_distribution(title=name, type_function=function, save=True)
            data.line['dash'] = 'dash'
        elif grafico == 'boxplot':
            data, fig = parcial5.plot_boxplot_resample(quantidade=100,
                                                      tempo_de_retorno=tempo_de_retorno,
                                                      save=True, name=name)
        return data, fig

    def sdp6(function, grafico, tempo_de_retorno):

        parcial6 = serie_vazao.parcial(station='XINGO',
                                      type_threshold='events_by_year',
                                      type_event='cheia',
                                      value_threshold=1.65,
                                      type_criterion='xmin_maior_dois_terco_x',
                                      duration=0)

        name = "SDP 6"
        if grafico == 'distribution':
            data, fig = parcial6.plot_distribution(title=name, type_function=function, save=True)
            data.line['dash'] = 'dashdot'
        elif grafico == 'boxplot':
            data, fig = parcial6.plot_boxplot_resample(quantidade=100,
                                                      tempo_de_retorno=tempo_de_retorno,
                                                      save=True, name=name)
        return data, fig

    def sdp7(function, grafico, tempo_de_retorno):
        parcial7 = serie_vazao.parcial(station='XINGO',
                                      type_threshold='stationary',
                                      type_event='cheia',
                                      value_threshold=0.75,
                                      type_criterion='mediana',
                                      duration=0)


        name = "SDP 7"
        #print(len(parcial.event_peaks()))
        #print(parcial.mvs())
        #print(parcial.peaks)
        if grafico == 'distribution':
            data, fig = parcial7.plot_distribution(title=name, type_function=function, save=True)
            data.line['dash'] = 'dot'
        elif grafico == 'boxplot':
            data, fig = parcial7.plot_boxplot_resample(quantidade=100,
                                                      tempo_de_retorno=tempo_de_retorno,
                                                      save=True, name=name)
        return data, fig

    def sdp8(function, grafico, tempo_de_retorno):

        parcial8 = serie_vazao.parcial(station='XINGO',
                                      type_threshold='stationary',
                                      type_event='cheia',
                                      value_threshold=0.75,
                                      type_criterion='xmin_maior_qmin',
                                      duration=0)

        name = "SDP 8"
        if grafico == 'distribution':
            data, fig = parcial8.plot_distribution(title=name, type_function=function, save=True)
            data.line['dash'] = 'dash'
        elif grafico == 'boxplot':
            data, fig = parcial8.plot_boxplot_resample(quantidade=100,
                                                      tempo_de_retorno=tempo_de_retorno,
                                                      save=True, name=name)
        return data, fig

    def sdp9(function, grafico, tempo_de_retorno):

        parcial9 = serie_vazao.parcial(station='XINGO',
                                      type_threshold='stationary',
                                      type_event='cheia',
                                      value_threshold=0.75,
                                      type_criterion='xmin_maior_dois_terco_x',
                                      duration=0)

        name = "SDP 9"
        if grafico == 'distribution':
            data, fig = parcial9.plot_distribution(title=name, type_function=function, save=True)
            data.line['dash'] = 'dashdot'
        elif grafico == 'boxplot':
            data, fig = parcial9.plot_boxplot_resample(quantidade=100,
                                                      tempo_de_retorno=tempo_de_retorno,
                                                      save=True, name=name)
        return data, fig


    data1, fig1 = sdp1(function=function, grafico='boxplot', tempo_de_retorno=[2])
    print("SDP1")
    pause()
    data2, fig2 = sdp2(function=function, grafico='boxplot', tempo_de_retorno=[2])
    print("SDP2")
    pause()
    data3, fig3 = sdp3(function=function, grafico='boxplot', tempo_de_retorno=[2])
    print("SDP3")
    pause()
    data4, fig4 = sdp4(function=function, grafico='boxplot', tempo_de_retorno=[2])
    print("SDP4")
    pause()
    data5, fig5 = sdp5(function=function, grafico='boxplot', tempo_de_retorno=[2])
    print("SDP5")
    pause()
    data6, fig6 = sdp6(function=function, grafico='boxplot', tempo_de_retorno=[2])
    print("SDP6")
    pause()
    data7, fig7 = sdp7(function=function, grafico='boxplot', tempo_de_retorno=[2])
    print("SDP7")
    pause()
    data8, fig8 = sdp8(function=function, grafico='boxplot', tempo_de_retorno=[2])
    print("SDP8")
    pause()
    data9, fig9 = sdp9(function=function, grafico='boxplot', tempo_de_retorno=[2])
    print("SDP9")
    pause()

    Boxplot(figs=[data1, data2, data3, data4, data5, data6, data7, data8, data9]).plot_comparasion()
    #Comparation_Distribution([data, data1, data2, data3], function, 'q75').plot()

    fim = timeit.default_timer()
    print('Duração: ', fim-ini)
