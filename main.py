import pandas as pd

from files.cemaden import Cemaden
from series.vazao import Vazao
from comparasion.rmse import RMSE
from comparasion.mae import MAE
from comparasion.rmae import RMAE

from graphics.comparation_distribution import Comparation_Distribution
from graphics.boxplot import Boxplot
import timeit

if __name__ == '__main__':
    ini = timeit.default_timer()
    #path = "/home/clebson/Documentos/Projetos/201405_output_horário"
    #dados = Cemaden(path)
    #print(dados.read())
    dados = pd.read_csv("dadosXingo.csv", index_col=0, names=[
                        "Data", "XINGO"], parse_dates=True)
    serie_vazao = Vazao(data=dados, font='ONS')
    serie_vazao.date(date_start='1/1/1999')
    maxima = serie_vazao.maximum('XINGO')
    data, fig = maxima.plot_distribution(title='SMA', estimador='mml',
                                         type_function='cumulative')
    parcial5 = serie_vazao.parcial(station='XINGO',
                                   type_threshold='events_by_year',
                                   type_event='cheia',
                                   type_criterion='duracao_e_xmin',
                                   value_threshold=1.65,
                                   duration=5)
    parcial7 = serie_vazao.parcial(station='XINGO',
                                   type_threshold='stationary',
                                   type_event='cheia',
                                   type_criterion='mediana',
                                   value_threshold=0.75,
                                   duration=0)
    data5, fig5 = parcial5.plot_distribution(title='SDP5', type_function='cumulative')
    data7, fig7 = parcial7.plot_distribution(title='SDP7', type_function='cumulative')
    data5['line']['dash'] = 'dot'
    data7['line']['dash'] = 'dash'
    Comparation_Distribution([data, data5, data7], type_function='cumulative', name='SMA x SDP').plot()
    #print(serie_vazao.plot_hydrogram('XINGO'))

    fim = timeit.default_timer()
    print('Duração: ', fim-ini)
