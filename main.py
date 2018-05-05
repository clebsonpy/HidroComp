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
        programPause = input("Press the <ENTER> key to continue...")

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
        return parcial.magnitude([2, 5, 10, 25, 50, 100, 500])
        #print(len(parcial.event_peaks()))
        #print(parcial.mvs())
        #print(parcial.peaks)
        #parcial.plot_hydrogram(name, save=True)
        #data, fig = parcial.plot_distribution(title=name, type_function=function, save=True)

    def sdp1(referencia, function, grafico):
        parcial1 = serie_vazao.parcial(station='XINGO',
                                      type_threshold='events_by_year',
                                      type_event='cheia',
                                      value_threshold=2.3,
                                      type_criterion='mediana',
                                      duration=0)

        name = "SDP 1"
        tempo_de_retorno = [2, 5, 10, 25, 50, 100, 500]
        mag_sdp1 = parcial1.magnitude_resample(quantidade=100,
                                               tempo_de_retorno=tempo_de_retorno)

        if grafico == 'distribution':
            data, fig = parcial1.plot_distribution(title=name, type_function=function,
                                                   save=True)
            data.line['dash'] = 'dot'

        elif grafico == 'boxplot':
            data, fig = parcial1.plot_boxplot_resample(magn_resample=mag_sdp1,
                                                        save=True, name=name)

        print(RMSE(reference=referencia, compared=mag_sdp1).quantify())
        print(MAE(reference=referencia, compared=mag_sdp1).quantify())
        print(RMAE(reference=referencia, compared=mag_sdp1).quantify())

        return data, fig

    def sdp2(referencia, function, grafico):

        parcial2 = serie_vazao.parcial(station='XINGO',
                                      type_threshold='events_by_year',
                                      type_event='cheia',
                                      value_threshold=2.3,
                                      type_criterion='xmin_maior_qmin',
                                      duration=0)

        name = "SDP 2"
        tempo_de_retorno = [2, 5, 10, 25, 50, 100, 500]
        mag_sdp2 = parcial2.magnitude_resample(quantidade=100,
                                               tempo_de_retorno=tempo_de_retorno)

        if grafico == 'distribution':
            data, fig = parcial2.plot_distribution(title=name, type_function=function, save=True)
            data.line['dash'] = 'dash'

        elif grafico == 'boxplot':
            data, fig = parcial2.plot_boxplot_resample(magn_resample=mag_sdp2,
                                                      save=True, name=name)

        print(RMSE(reference=referencia, compared=mag_sdp2).quantify())
        print(MAE(reference=referencia, compared=mag_sdp2).quantify())
        print(RMAE(reference=referencia, compared=mag_sdp2).quantify())

        return data, fig

    def sdp3(referencia, function, grafico):

        parcial3 = serie_vazao.parcial(station='XINGO',
                                      type_threshold='events_by_year',
                                      type_event='cheia',
                                      value_threshold=2.3,
                                      type_criterion='xmin_maior_dois_terco_x',
                                      duration=0)

        name = "SDP 3"
        tempo_de_retorno = [2, 5, 10, 25, 50, 100, 500]
        mag_sdp3 = parcial3.magnitude_resample(quantidade=100,
                                               tempo_de_retorno=tempo_de_retorno)

        if grafico == 'distribution':
            data, fig = parcial3.plot_distribution(title=name, type_function=function, save=True)
            data.line['dash'] = 'dashdot'

        elif grafico == 'boxplot':
            data, fig = parcial3.plot_boxplot_resample(magn_resample=mag_sdp3,
                                                      save=True, name=name)

        print(RMSE(reference=referencia, compared=mag_sdp3).quantify())
        print(MAE(reference=referencia, compared=mag_sdp3).quantify())
        print(RMAE(reference=referencia, compared=mag_sdp3).quantify())

        return data, fig

    def sdp4(referencia, function, grafico):
        parcial4 = serie_vazao.parcial(station='XINGO',
                                      type_threshold='events_by_year',
                                      type_event='cheia',
                                      value_threshold=1.65,
                                      type_criterion='mediana',
                                      duration=0)


        name = "SDP 4"
        tempo_de_retorno = [2, 5, 10, 25, 50, 100, 500]
        mag_sdp4 = parcial4.magnitude_resample(quantidade=100,
                                               tempo_de_retorno=tempo_de_retorno)

        if grafico == 'distribution':
            data, fig = parcial4.plot_distribution(title=name, type_function=function, save=True)
            data.line['dash'] = 'dot'

        elif grafico == 'boxplot':
            data, fig = parcial4.plot_boxplot_resample(magn_resample=mag_sdp4,
                                                      save=True, name=name)

        print(RMSE(reference=referencia, compared=mag_sdp4).quantify())
        print(MAE(reference=referencia, compared=mag_sdp4).quantify())
        print(RMAE(reference=referencia, compared=mag_sdp4).quantify())

        return data, fig

    def sdp5(referencia, function, grafico):

        parcial5 = serie_vazao.parcial(station='XINGO',
                                      type_threshold='events_by_year',
                                      type_event='cheia',
                                      value_threshold=1.65,
                                      type_criterion='xmin_maior_qmin',
                                      duration=0)

        name = "SDP 5"
        tempo_de_retorno = [2, 5, 10, 25, 50, 100, 500]
        mag_sdp5 = parcial5.magnitude_resample(quantidade=100,
                                               tempo_de_retorno=tempo_de_retorno)

        if grafico == 'distribution':
            data, fig = parcial5.plot_distribution(title=name, type_function=function, save=True)
            data.line['dash'] = 'dash'
        elif grafico == 'boxplot':
            data, fig = parcial5.plot_boxplot_resample(magn_resample=mag_sdp5,
                                                      save=True, name=name)

        print(RMSE(reference=referencia, compared=mag_sdp5).quantify())
        print(MAE(reference=referencia, compared=mag_sdp5).quantify())
        print(RMAE(reference=referencia, compared=mag_sdp5).quantify())

        return data, fig

    def sdp6(referencia, function, grafico):

        parcial6 = serie_vazao.parcial(station='XINGO',
                                      type_threshold='events_by_year',
                                      type_event='cheia',
                                      value_threshold=1.65,
                                      type_criterion='xmin_maior_dois_terco_x',
                                      duration=0)

        name = "SDP 6"
        tempo_de_retorno = [2, 5, 10, 25, 50, 100, 500]
        mag_sdp6 = parcial6.magnitude_resample(quantidade=100,
                                               tempo_de_retorno=tempo_de_retorno)

        if grafico == 'distribution':
            data, fig = parcial6.plot_distribution(title=name, type_function=function, save=True)
            data.line['dash'] = 'dashdot'
        elif grafico == 'boxplot':
            data, fig = parcial6.plot_boxplot_resample(magn_resample=mag_sdp6,
                                                      save=True, name=name)

        print(RMSE(reference=referencia, compared=mag_sdp6).quantify())
        print(MAE(reference=referencia, compared=mag_sdp6).quantify())
        print(RMAE(reference=referencia, compared=mag_sdp6).quantify())
        return data, fig

    def sdp7(referencia, function, grafico):
        parcial7 = serie_vazao.parcial(station='XINGO',
                                      type_threshold='stationary',
                                      type_event='cheia',
                                      value_threshold=0.75,
                                      type_criterion='mediana',
                                      duration=0)


        name = "SDP 7"
        tempo_de_retorno = [2, 5, 10, 25, 50, 100, 500]
        mag_sdp7 = parcial7.magnitude_resample(quantidade=100,
                                               tempo_de_retorno=tempo_de_retorno)

        if grafico == 'distribution':
            data, fig = parcial7.plot_distribution(title=name, type_function=function, save=True)
            data.line['dash'] = 'dot'
        elif grafico == 'boxplot':
            data, fig = parcial7.plot_boxplot_resample(magn_resample=mag_sdp7,
                                                      save=True, name=name)
        print(RMSE(reference=referencia, compared=mag_sdp7).quantify())
        print(MAE(reference=referencia, compared=mag_sdp7).quantify())
        print(RMAE(reference=referencia, compared=mag_sdp7).quantify())
        return data, fig

    def sdp8(referencia, function, grafico):

        parcial8 = serie_vazao.parcial(station='XINGO',
                                      type_threshold='stationary',
                                      type_event='cheia',
                                      value_threshold=0.75,
                                      type_criterion='xmin_maior_qmin',
                                      duration=0)

        name = "SDP 8"
        tempo_de_retorno = [2, 5, 10, 25, 50, 100, 500]
        mag_sdp8 = parcial8.magnitude_resample(quantidade=100,
                                               tempo_de_retorno=tempo_de_retorno)
        if grafico == 'distribution':
            data, fig = parcial8.plot_distribution(title=name, type_function=function, save=True)
            data.line['dash'] = 'dash'
        elif grafico == 'boxplot':
            data, fig = parcial8.plot_boxplot_resample(magn_resample=mag_sdp8,
                                                       save=True, name=name)

        print(RMSE(reference=referencia, compared=mag_sdp8).quantify())
        print(MAE(reference=referencia, compared=mag_sdp8).quantify())
        print(RMAE(reference=referencia, compared=mag_sdp8).quantify())
        return data, fig

    def sdp9(referencia, function, grafico):

        parcial9 = serie_vazao.parcial(station='XINGO',
                                      type_threshold='stationary',
                                      type_event='cheia',
                                      value_threshold=0.75,
                                      type_criterion='xmin_maior_dois_terco_x',
                                      duration=0)

        name = "SDP 9"
        tempo_de_retorno = [2, 5, 10, 25, 50, 100, 500]
        mag_sdp9 = parcial9.magnitude_resample(quantidade=100,
                                               tempo_de_retorno=tempo_de_retorno)
        print(RMSE(reference=referencia, compared=mag_sdp9).quantify())
        print(MAE(reference=referencia, compared=mag_sdp9).quantify())
        print(RMAE(reference=referencia, compared=mag_sdp9).quantify())
        if grafico == 'distribution':
            data, fig = parcial9.plot_distribution(title=name, type_function=function,
                                                   save=True)
            data.line['dash'] = 'dashdot'
        elif grafico == 'boxplot':
            data, fig = parcial9.plot_boxplot_resample(magn_resample=mag_sdp9,
                                                       save=True, name=name)
        return data, fig

    magn_ref = referencia(function=function)

    data1, fig1 = sdp1(referencia=magn_ref, function=function,
                       grafico='boxplot')
    print("SDP1")
    pause()
    data2, fig2 = sdp2(referencia=magn_ref, function=function,
                       grafico='boxplot')
    print("SDP2")
    pause()

    data3, fig3 = sdp3(referencia=magn_ref, function=function,
                       grafico='boxplot')
    print("SDP3")
    pause()

    data4, fig4 = sdp4(referencia=magn_ref, function=function,
                       grafico='boxplot')
    print("SDP4")
    pause()
    data5, fig5 = sdp5(referencia=magn_ref, function=function,
                       grafico='boxplot')
    print("SDP5")
    pause()

    data6, fig6 = sdp6(referencia=magn_ref, function=function,
                       grafico='boxplot')
    print("SDP6")
    pause()

    data7, fig7 = sdp7(referencia=magn_ref, function=function,
                       grafico='boxplot')
    print("SDP7")
    pause()

    data8, fig8 = sdp8(referencia=magn_ref, function=function,
                       grafico='boxplot')
    print("SDP8")
    pause()
    data9, fig9 = sdp9(referencia=magn_ref, function=function,
                       grafico='boxplot')
    print("SDP9")
    pause()


    #Tempo2
    data1[0].name = 'SDP 1'
    data2[0].name = 'SDP 2'
    data3[0].name = 'SDP 3'
    data4[0].name = 'SDP 4'
    data5[0].name = 'SDP 5'
    data6[0].name = 'SDP 6'
    data7[0].name = 'SDP 7'
    data8[0].name = 'SDP 8'
    data9[0].name = 'SDP 9'

    box0 = [data1[0], data2[0], data3[0], data4[0], data5[0],
            data6[0], data7[0], data8[0], data9[0]]

    Boxplot(figs=box0).plot_comparasion()
    pause()

    #Tempo5
    data1[1].name = 'SDP 1'
    data2[1].name = 'SDP 2'
    data3[1].name = 'SDP 3'
    data4[1].name = 'SDP 4'
    data5[1].name = 'SDP 5'
    data6[1].name = 'SDP 6'
    data7[1].name = 'SDP 7'
    data8[1].name = 'SDP 8'
    data9[1].name = 'SDP 9'

    box1 = [data1[1], data2[1], data3[1], data4[1], data5[1],
            data6[1], data7[1], data8[1], data9[1]]

    Boxplot(figs=box1).plot_comparasion()
    pause()

    #Tempo10
    data1[2].name = 'SDP 1'
    data2[2].name = 'SDP 2'
    data3[2].name = 'SDP 3'
    data4[2].name = 'SDP 4'
    data5[2].name = 'SDP 5'
    data6[2].name = 'SDP 6'
    data7[2].name = 'SDP 7'
    data8[2].name = 'SDP 8'
    data9[2].name = 'SDP 9'

    box2 = [data1[2], data2[2], data3[2], data4[2], data5[2], data6[2],
            data7[2], data8[2], data9[2]]

    Boxplot(figs=box2).plot_comparasion()
    pause()

    #Tempo25
    data1[3].name = 'SDP 1'
    data2[3].name = 'SDP 2'
    data3[3].name = 'SDP 3'
    data4[3].name = 'SDP 4'
    data5[3].name = 'SDP 5'
    data6[3].name = 'SDP 6'
    data7[3].name = 'SDP 7'
    data8[3].name = 'SDP 8'
    data9[3].name = 'SDP 9'

    box3 = [data1[3], data2[3], data3[3], data4[3], data5[3], data6[3],
            data7[3], data8[3], data9[3]]
    Boxplot(figs=box3).plot_comparasion()
    pause()

    #Tempo50
    data1[4].name = 'SDP 1'
    data2[4].name = 'SDP 2'
    data3[4].name = 'SDP 3'
    data4[4].name = 'SDP 4'
    data5[4].name = 'SDP 5'
    data6[4].name = 'SDP 6'
    data7[4].name = 'SDP 7'
    data8[4].name = 'SDP 8'
    data9[4].name = 'SDP 9'

    box4 = [data1[4], data2[4], data3[4], data4[4], data5[4],
            data6[4], data7[4], data8[4], data9[4]]

    Boxplot(figs=box4).plot_comparasion()
    pause()

    #Tempo100
    data1[5].name = 'SDP 1'
    data2[5].name = 'SDP 2'
    data3[5].name = 'SDP 3'
    data4[5].name = 'SDP 4'
    data5[5].name = 'SDP 5'
    data6[5].name = 'SDP 6'
    data7[5].name = 'SDP 7'
    data8[5].name = 'SDP 8'
    data9[5].name = 'SDP 9'

    box5 = [data1[5], data2[5], data3[5], data4[5], data5[5],
            data6[5], data7[5], data8[5], data9[5]]
    Boxplot(figs=box5).plot_comparasion()
    pause()

    #Tempo500
    data1[6].name = 'SDP 1'
    data2[6].name = 'SDP 2'
    data3[6].name = 'SDP 3'
    data4[6].name = 'SDP 4'
    data5[6].name = 'SDP 5'
    data6[6].name = 'SDP 6'
    data7[6].name = 'SDP 7'
    data8[6].name = 'SDP 8'
    data9[6].name = 'SDP 9'

    box6 = [data1[6], data2[6], data3[6], data4[6], data5[6],
            data6[6], data7[6], data8[6], data9[6]]
    Boxplot(figs=box6).plot_comparasion()

    #Comparation_Distribution([data, data1, data2, data3], function, 'q75').plot()
    
    fim = timeit.default_timer()
    print('Duração: ', fim-ini)
