import os

import plotly as py
import timeit
import pandas as pd
import geopandas

import matplotlib.pyplot as plt
from hydrocomp.api_ana.inventario import Inventario
from hydrocomp.api_ana.basin import Basin
from hydrocomp.iha import iha
from hydrocomp.iha.iha import IHA
from hydrocomp.iha.graphics import Graphics
from hydrocomp.series.flow import Flow
from hydrocomp.series.cota import Cota
from hydrocomp.series.rainfall import Rainfall

if __name__ == '__main__':
    ini = timeit.default_timer()
    # Boa Fortuna
    """
    path = '/home/clebsonpy/Dropbox/IHA_Dados/Dados/Boa Fortuna'
    file = os.path.abspath(os.path.join(path, "vazoes_T_39770000.txt"))
    flow = Flow(path=file, source='ANA', station='39770000_FLU')
    figg = flow.gantt(name='Gantt')

    flow.date(date_start='01/01/1974', date_end='31/12/1988')
    flow.data.to_csv(os.path.join(path, 'dados/boa_fortuna_74_88.csv'))

    q90 = flow.data.quantile(0.1)
    figp, datap = flow.permanence_curve()
    fig_year, data3 = flow.hydrogram_year()

    flow = Flow(path=file, source='ANA', station='39770000_FLU')
    flow.date(date_start='01/01/1990', date_end='31/12/2009')
    flow.data.to_csv(os.path.join(path, 'dados/boa_fortuna_90_09.csv'))
    flow_1 = flow.simulation_withdraw(criterion='q90', rate=50, value=q90, months=[11, 12, 1, 2, 3, 4])
    flow_1.to_csv(os.path.join(path, 'dados/boa_fortuna_withdraw_50_11_4.csv'))
    flow_2 = flow.simulation_withdraw(criterion='q90', rate=70, value=q90, months=[11, 12, 1, 2, 3, 4])
    flow_2.to_csv(os.path.join(path, 'dados/boa_fortuna_withdraw_70_11_4.csv'))
    flow_3 = flow.simulation_withdraw(criterion='q90', rate=50, value=q90)
    flow_3.to_csv(os.path.join(path, 'dados/boa_fortuna_withdraw_50_all.csv'))
    flow_4 = flow.simulation_withdraw(criterion='q90', rate=70, value=q90)
    flow_4.to_csv(os.path.join(path, 'dados/boa_fortuna_withdraw_70_all.csv'))

    flow = Flow(data=flow.data.combine_first(flow_1).combine_first(flow_2).combine_first(flow_3).combine_first(flow_4))
    figh, data = flow.hydrogram()
    """

    # Cachoeira Morena
    """
    path = '/home/clebsonpy/Dropbox/IHA_Dados/Dados/Cach. Morena'
    file = os.path.abspath(os.path.join(path, "vazoes_T_16100000.txt"))
    flow = Flow(path=file, source='ANA', station='16100000_FLU')
    figg = flow.gantt(name='Gantt')

    flow_pre = Flow(path=file, source='ANA', station='16100000_FLU')
    flow_pre.date(date_start='1/11/1973', date_end='31/10/1986')
    flow_pre.data.rename(columns={'16100000_FLU': '16100000_PRE'}, inplace=True)
    flow_pre.station = '16100000_PRE'
    flow_pre.data.to_csv(os.path.join(path, 'dados/cach_morena_73_86_pre.csv'))
    fig_year, data3 = flow_pre.hydrogram_year()

    flow_pos = Flow(path=file, source='ANA', station='16100000_FLU')
    flow_pos.date(date_start='1/11/1993', date_end='31/10/2005')
    flow_pos.data.rename(columns={'16100000_FLU': '16100000_POS'}, inplace=True)
    flow_pos.station = '16100000_POS'
    flow_pos.data.to_csv(os.path.join(path, 'dados/cach_morena_93_05_pos.csv'))

    flow = Flow(data=flow.data.combine_first(flow_pre.data).combine_first(flow_pos.data))
    figh, data = flow.hydrogram()
    """

    # Raizama
    """
    path = '/home/clebsonpy/Dropbox/IHA_Dados/Dados/Raizama'
    file = os.path.abspath(os.path.join(path, "vazoes_T_66231000.txt"))
    flow = Flow(path=file, source='ANA', station='66231000_FLU')
    figg = flow.gantt(name='Gantt')


    flow_pre = Flow(path=file, source='ANA', station='66231000_FLU')
    flow_pre.date(date_start='01/08/1981', date_end='31/07/1990')
    flow_pre.data.rename(columns={'66231000_FLU': '66231000_PRE'}, inplace=True)
    flow_pre.station = '66231000_PRE'
    flow_pre.data.to_csv(os.path.join(path, 'dados/raizama_81_90_pre.csv'))
    fig_year, data3 = flow_pre.hydrogram_year()

    flow_pos = Flow(path=file, source='ANA', station='66231000_FLU')
    flow_pos.date(date_start='01/08/2000', date_end='31/07/2004')
    flow_pos.data.rename(columns={'66231000_FLU': '66231000_POS'}, inplace=True)
    flow_pos.station = '66231000_POS'
    flow_pos.data.to_csv(os.path.join(path, 'dados/raizama_00_04_pos.csv'))


    flow = Flow(data=flow.data.combine_first(flow_pre.data).combine_first(flow_pos.data))
    figh, data = flow.hydrogram()
    """

    # Rosário Oeste
    """
    path = '/home/clebsonpy/Dropbox/IHA_Dados/Dados/Rosário Oeste'
    file = os.path.abspath(os.path.join(path, "vazoes_T_66250001.txt"))
    flow = Flow(path=file, source='ANA', station='66250001_FLU')
    figg = flow.gantt(name='Gantt')

    flow_pre = Flow(path=file, source='ANA', station='66250001_FLU')
    flow_pre.date(date_start='01/08/1981', date_end='31/07/1990')
    flow_pre.data.rename(columns={'66250001_FLU': '66250001_PRE'}, inplace=True)
    flow_pre.station = '66250001_PRE'
    flow_pre.data.to_csv(os.path.join(path, 'dados/Rosário Oeste_81_90_pre.csv'))
    fig_year, data3 = flow_pre.hydrogram_year()

    flow_pos = Flow(path=file, source='ANA', station='66250001_FLU')
    flow_pos.date(date_start='01/08/2000', date_end='31/07/2007')
    flow_pos.data.rename(columns={'66250001_FLU': '66250001_POS'}, inplace=True)
    flow_pos.station = '66250001_POS'
    flow_pos.data.to_csv(os.path.join(path, 'dados/Rosário Oeste_00_04_pos.csv'))

    flow = Flow(data=flow.data.combine_first(flow_pre.data).combine_first(flow_pos.data))
    figh, data = flow.hydrogram()
    """

    # Xingó
    """
    path = '/home/clebsonpy/Dropbox/IHA_Dados/Dados/Xingó'

    file_nat = os.path.abspath(os.path.join(path, 'Xingo_Nat.csv'))
    dados_nat = pd.read_csv(file_nat, index_col=0, parse_dates=True)
    dados_nat.rename(columns={'Flow': "Natural"}, inplace=True)
    flow_nat = Flow(data=dados_nat, station='Natural')
    fig_year, data3 = flow_nat.hydrogram_year()
    flow_nat.date(date_start='01/09/1995', date_end='31/08/2008')
    flow_nat.data.to_csv(os.path.join(path, 'dados/Xingo_Nat.csv'))

    file_obs = os.path.abspath(os.path.join(path, 'Xingo_Obs.csv'))
    flow_obs = pd.read_csv(file_obs, index_col=0, parse_dates=True)
    flow_obs.rename(columns={'Flow': "Observada"}, inplace=True)
    flow_obs = Flow(data=flow_obs, station="Observada")
    flow_obs.date(date_start='01/09/1995', date_end='31/08/2008')
    flow_obs.data.to_csv(os.path.join(path, 'dados/Xingo_Obs.csv'))

    flow = Flow(data=flow_nat.data.combine_first(flow_obs.data))
    print(flow)
    figh, data = flow.hydrogram()
    """

    # Porto Primavera
    """
    path = '/home/clebsonpy/Dropbox/IHA_Dados/Dados/Porto Primavera'

    file_nat = os.path.abspath(os.path.join(path, 'porto_primavera_nat.csv'))
    dados_nat = pd.read_csv(file_nat, index_col=0, parse_dates=True)
    dados_nat.rename(columns={'P. PRIMAVERA': "Natural"}, inplace=True)
    flow_nat = Flow(data=dados_nat, station='Natural')
    fig_year, data3 = flow_nat.hydrogram_year()
    flow_nat.date(date_start='01/09/1998', date_end='31/08/2011')
    flow_nat.data.to_csv(os.path.join(path, 'dados/porto_primavera_nat.csv'))

    file_obs = os.path.abspath(os.path.join(path, 'porto_primavera_obs.csv'))
    dados_obs = pd.read_csv(file_obs, index_col=0, parse_dates=True)
    dados_obs.rename(columns={'Vazão Defluente Média (m³/s)': "Observada"}, inplace=True)
    flow_obs = Flow(data=dados_obs, station="Observada")
    flow_obs.date(date_start='01/09/1998', date_end='31/08/2011')
    flow_obs.data.to_csv(os.path.join(path, 'dados/porto_primavera_obs.csv'))

    flow = Flow(data=flow_nat.data.combine_first(flow_obs.data))
    figh, data = flow.hydrogram()
    """

    """
    path = ''
    file = os.path.abspath(os.path.join(path, 'rio_ibicui_consistido.csv'))

    for name in ['76077000', '76085000', '76100000', '76120000', '76251000', '76260000', '76300000', '76310000',
                 '76360001', '76370000', '76380000', '76395000', '76431000', '76440000', '76460000', '76490000',
                 '76500000', '76550000', '76560000', '76600000', '76630000', '76650000', '76700000', '76742000',
                 '76745000', '76750000', '76800000', '76081000']:
        data = pd.read_csv(file, parse_dates=True, index_col=0)
        print(name)
        station = '{}_FLU'.format(name)

        flow = Flow(data=data,  station=station)
        fig_year, data = flow.hydrogram_year(title=station)
        py.offline.plot(fig_year, filename=os.path.join(path, 'gráficos/hidrograma_year_{}.html'.format(name)))
    """

    # dados.data.to_csv("rio_ibicui_consistido.csv")
    # print(dados['1993'])
    # file = os.path.abspath(os.path.join('Medicoes', 'dadosXingo_nat.csv'))
    # dados = pd.read_csv(file, index_col=0, parse_dates=True)
    # print(dados)
    """
    path = ''
    stations = ['76100000', '76310000', '76380000', '76440000', '76460000', '76750000', '76800000']
    #stations = ['76077000', '76085000', '76100000', '76120000', '76251000', '76260000', '76300000', '76310000',
    #            '76360001', '76370000', '76380000', '76395000', '76431000', '76440000', '76460000', '76490000',
    #            '76500000', '76550000', '76560000', '76600000', '76630000', '76650000', '76700000', '76742000',
    #            '76745000', '76750000', '76800000', '76081000']
    flow = Flow(path_file=stations, source='ANA', consistence=1)
    flow.date(date_end='31/12/1977', date_start='1/1/1968')
    flow.station = '76100000'
    max_flow = flow.maximum()
    print(max_flow.obj.month_abr)
    print(max_flow.peaks)
    fig, data = max_flow.hydrogram()
    #figg, data = flow.gantt(name='gantt')
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
    #py.offline.plot(fig2, filename=os.path.join(path, 'gráficos/rva.html'))

    py.offline.plot(fig_spells_nat, filename=os.path.join(path, 'gráficos/spells_nat.html'))
    py.offline.plot(fig_h, filename=os.path.join(path, 'gráficos/hidro.html'))
    #py.offline.plot(fig_hp, filename=os.path.join(path, 'gráficos/hidro_parcial.html'))
    #py.offline.plot(fig, filename=os.path.join(path, 'gráficos/permanência.html'))

    fim = timeit.default_timer()

    print('Duração: ', fim - ini)
