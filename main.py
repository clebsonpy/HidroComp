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

    # Rosario Oeste
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

    # Xingo
    """
    path = '/home/clebsonpy/Dropbox/IHA_Dados/Dados/Xingo'

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
    path = ''
    #file_rain = os.path.abspath(os.path.join('Medicoes', 'dados_inmet.csv'))
    # dados = pd.read_csv(file, ',', index_col=0, parse_dates=True).NAT
    #rainfall = Rainfall(data=dados, source='INMET')
    #print(rainfall.data)
    #stations = ['76100000', '76310000', '76380000', '76440000', '76460000', '76750000', '76800000']

    #df = SerieTemporal().get(codEstacao='76100000', tipoDados='3')
    #print(df)
    #stations_rainfall = ['835000', '835002', '835014', '835015', '835025', '835026', '835042', '835043', '835050',
    #                     '835112', '835116', '835119', '835140', '835142', '835150', '835152', '835155', '835157',
    #                     '835158', '835160', '835177', '835179', '835181', '835186', '835195', '835197', '835198',
    #                     '835203', '835209']

    #stations = ['76077000', '76085000', '76100000', '76120000', '76251000', '76260000', '76300000', '76310000',
    #            '76360001', '76370000', '76380000', '76395000', '76431000', '76440000', '76460000', '76490000',
    #            '76500000', '76550000', '76560000', '76600000', '76630000', '76650000', '76700000', '76742000',
    #            '76745000', '76750000', '76800000', '76081000']

    #stations = ['49775100', '49775000', '49760000', '49750000', '49743100', '49740000', '49723000', '49706000',
    #            '49690000', '49670000', '49550000', '49390000', '49370000', '49369000', '49330000', '49208100']

    stations = ['49151800', '49169000', '49270000', '49280000', '49295000', '49305000', '49310000', '49310040',
                '49310060', '49310900', '49315000', '49330000', '49330001', '49330002', '49330990', '49340000',
                '49340010', '49340020', '49340030', '49340040', '49340050', '49340060', '49340070', '49340080',
                '49340100', '49341000', '49369000', '49370000', '49370001', '49370002', '49402000', '49402500',
                '49047000', '49050002', '49180000', '49190000', '49200000', '49205000', '49208020', '49208030',
                '49208040', '49208050', '49208055', '49208070', '49208080', '49208090', '49208100', '49209000',
                '49209100', '49210000', '49210040', '49210045', '49210050', '49210060', '49210070', '49210075',
                '49210080', '49210085', '49210090', '49211010', '49211020', '49211030', '49211040', '49215000',
                '49330970', '49330980', '49340200', '49369600', '49385000', '49390000', '49550000', '49570000',
                '49572000', '49598900', '49601000', '49610000', '49619000', '49620000', '49650000', '49658000',
                '49660000', '49660001', '49660002', '49670000', '49681900', '49690000', '49695000', '49700000',
                '49704000', '49704900', '49705000', '49705001', '49705005', '49706000', '49706250', '49720000',
                '49723000', '49730000', '49731000', '49731100', '49731110', '49740000', '49740001', '49743000',
                '49743100', '49744000', '49745000', '49746000', '49747000', '49750000', '49760000', '49775000',
                '49775100', '49775110', '49775120', '49790000', '49790001']

    flow = Flow(station='49330000', source='ANA')
    flow.data.to_csv('Dados-Vazao-SF-AL-SE.csv')
    # flow.date(date_end='31/12/1977', date_start='1/4/1968')
    # flow.station = '76100000'
    # max_flow = flow.maximum()
    # print(max_flow.obj.month_abr)
    #parcial_flow = flow.parcial(type_criterion='autocorrelation', type_threshold="stationary",
                            #    type_event="drought", value_threshold=0.25, duration=6)
    fig, data = flow.gantt('Gantt')
    # print(max_flow.peaks)
    # fig, data = max_flow.polar()
    # fig, data = parcial_flow.hydrogram(title="Hidrograma")
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
    #py.offline.plot(fig, filename=os.path.join(path, 'graficos/hidro.html'))
    #py.offline.plot(fig, filename=os.path.join(path, 'graficos/gantt_nubia.html'))
    # py.offline.plot(fig_hp, filename=os.path.join(path, 'graficos/hidro_parcial.html'))
    # py.offline.plot(fig, filename=os.path.join(path, 'graficos/permanencia.html'))

    fim = timeit.default_timer()

    print('Duracao: ', fim - ini)
