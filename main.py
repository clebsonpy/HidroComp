import os

import plotly as py
import timeit
import pandas as pd

from hydrocomp.api_ana.inventario import Inventario
from hydrocomp.api_ana.basin import Basin
from hydrocomp.api_ana.serie_temporal import SerieTemporal
from hydrocomp.iha import iha
from hydrocomp.iha.iha import IHA
from hydrocomp.iha.graphics import Graphics
from hydrocomp.series.flow import Flow
from hydrocomp.series.height import Height
from hydrocomp.series.rainfall import Rainfall

if __name__ == '__main__':
    ini = timeit.default_timer()

    # dados.data.to_csv("rio_ibicui_consistido.csv")
    # print(dados['1993'])
    file = os.path.abspath(os.path.join('Medicoes', 'dadosXingo_nat.csv'))
    # dados = pd.read_csv(file, index_col=0, parse_dates=True)
    # print(dados)
    path = ''
    #file_rain = os.path.abspath(os.path.join('Medicoes', 'dados_inmet.csv'))
    dados = pd.read_csv(file, ',', index_col=0, parse_dates=True).NAT
    #rainfall = Rainfall(data=dados, source='INMET')
    #print(rainfall.data)
    #stations = ['76100000', '76310000', '76380000', '76440000', '76460000', '76750000', '76800000']

    #df = SerieTemporal().get(codEstacao='76100000', tipoDados='3')
    #print(df)
    #stations_rainfall = ['835000', '835002', '835014', '835015', '835025', '835026', '835042', '835043', '835050',
    #                     '835112', '835116', '835119', '835140', '835142', '835150', '835152', '835155', '835157',
    #                     '835158', '835160', '835177', '835179', '835181', '835186', '835195', '835197', '835198',
    #                     '835203', '835209']

    # stations = ['76077000', '76085000', '76100000', '76120000', '76251000', '76260000', '76300000', '76310000',
    #            '76360001', '76370000', '76380000', '76395000', '76431000', '76440000', '76460000', '76490000',
    #            '76500000', '76550000', '76560000', '76600000', '76630000', '76650000', '76700000', '76742000',
    #            '76745000', '76750000', '76800000', '76081000']
    flow = Flow(data=dados, station='Observados')
    #flow.date(date_end='31/12/1977', date_start='1/4/1968')
    #flow.station = '76100000'
    #max_flow = flow.maximum()
    # print(max_flow.obj.month_abr)
    # print(max_flow.peaks)
    fig, data = flow.hydrogram_year(title="Hidrograma", threshold=3500)
    #print(max_flow.peaks)
    #figg, data = flow.gantt(name='gantt')
    #fig_h, data = flow.plot_hydrogram('Hidro')
    """

    path = ''
    file_obs = os.path.abspath(os.path.join('Medicoes', 'dadosXingo_obs.csv'))
    file_nat = os.path.abspath(os.path.join('Medicoes', 'dadosXingo_obs.csv'))

    data_obs = pd.read_csv(file_obs, ',', index_col=0, parse_dates=True)
    data_nat = pd.read_csv(file_nat, ',', index_col=0, parse_dates=True)

    threshold_high = data_nat.quantile(0.75).values[0]
    threshold_low = data_nat.quantile(0.25).values[0]
    print('Threshold High: {}'.format(threshold_high))
    print('Threshold Low: {}'.format(threshold_low))

    iha_obj_nat = IHA(data_nat, month_water=9, status='pre', statistic='non-parametric', central_metric='mean',
                      variation_metric='cv', type_criterion=None, type_threshold="stationary", duration=0,
                      threshold_high=threshold_high, threshold_low=threshold_low, source='ONS', station='NAT')

    iha_obj_obs = IHA(data_obs, month_water=9, status='pos', statistic='non-parametric', central_metric='mean',
                      variation_metric='cv', type_criterion=None, type_threshold="stationary", duration=0,
                      threshold_high=threshold_high, threshold_low=threshold_low, source='CHESF', station='OBS')

    
    data_group_nat, metric_nat, events_nat_high, events_nat_low = iha_obj_nat.frequency_and_duration()
    data_group_obs, metric_obs, events_obs_high, events_obs_low = iha_obj_obs.frequency_and_duration()

    #print(metric_nat)
    #print(metric_obs)

    #line = iha_obj_nat.rva_line(data_group_nat, boundaries=17)

    #fig_obs, data_obs = Graphics(data_group_obs, status=iha_obj_obs.status).plot(metric='Date of minimum',
    #                                                                             line=line, color='red')
    #fig_nat, data_nat = Graphics(data_group_nat, status=iha_obj_nat.status).plot(metric='Date of minimum',
    #                                                                             line=line, color='blue')
    #fig2 = dict(data=data_obs + [data_nat[0]], layout=fig_nat['layout'])
    #fig_hp, data_hp = events_obs_low.plot_hydrogram("Parcial")
    fig_h = iha_obj_nat.flow.hydrogram_year("Hidrograma")
    fig_spells_nat, df = events_nat_high.plot_spells("Observado")
    # fig_spells_obs = partial_high_obs.plot_spells("Obs")
    # test = dados.date(date_start="01/01/1995", date_end="31/12/2012")
    # value_threshold = test.mean()['XINGO'] + test.std()['XINGO']
    # print(test.mean())
    # maximum = test.maximum(station='MANSO')
    # print(maximum.dist_gev.mvs())
    # parcial = flow.parcial(station="XINGO", type_criterion='autocorrelation', type_threshold="stationary", type_event="flood",
    #                        value_threshold=0.75, duration=6)
    # print(parcial.peaks)
    # print(parcial.threshold)
    # print(parcial.test_autocorrelation())

    # flow.data.to_csv('caracarai.csv')
    # fig, data = parcial.plot_hydrogram('Parcial')
    #py.offline.plot(fig2, filename=os.path.join(path, 'graficos/rva.html'))
    """
    #py.offline.plot(figg, filename=os.path.join(path, 'graficos/gantt_test.html'))
    py.offline.plot(fig, filename=os.path.join(path, 'graficos/hidro.html'))
    # py.offline.plot(fig_hp, filename=os.path.join(path, 'graficos/hidro_parcial.html'))
    # py.offline.plot(fig, filename=os.path.join(path, 'graficos/permanencia.html'))

    fim = timeit.default_timer()

    print('Duracao: ', fim - ini)
