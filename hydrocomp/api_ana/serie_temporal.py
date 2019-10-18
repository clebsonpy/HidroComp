import pandas as pd
import calendar as ca
from hydrocomp.api_ana.api_biuld import ApiBiuld


class SerieTemporal(ApiBiuld):
    url = 'http://telemetriaws1.ana.gov.br/ServiceANA.asmx/HidroSerieHistorica'
    params = {'codEstacao': '', 'dataInicio': '', 'dataFim': '', 'tipoDados': '', 'nivelConsistencia': ''}
    typesData = {'3': ['Vazao{:02}'], '2': ['Chuva{:02}'], '1': ['Cota{:02}']}

    def __multIndex(self, date, n_days, consistence):
        list_date = pd.date_range(date, periods=n_days, freq="D")
        list_cons = [int(consistence)] * n_days
        index_multi = list(zip(*[list_date, list_cons]))
        return pd.MultiIndex.from_tuples(index_multi, names=["Date", "Consistence"])

    def get(self, **kwargs):

        super().get(**kwargs)

        self.params.update(kwargs)
        root = self.requests()
        series = []
        for month in root.iter('SerieHistorica'):
            vazao = []
            codigo = month.find('EstacaoCodigo').text
            date_str = month.find('DataHora').text
            date = pd.to_datetime(date_str, dayfirst=True)
            days = ca.monthrange(date.year, date.month)[1]
            consistence = month.find('NivelConsistencia').text
            if date.day == 1:
                n_days = days
            else:
                n_days = days - date.day
            date_idx = self.__multIndex(date, n_days, consistence)
            for i in range(1, n_days+1):
                value = self.typesData[self.params['tipoDados']][0].format(i)
                try:
                    vazao.append(float(month.find(value).text))
                except TypeError:
                    vazao.append(month.find(value).text)
                except AttributeError:
                    vazao.append(None)
            series.append(pd.Series(vazao, index=date_idx, name=codigo))
        try:
            data_flow = pd.DataFrame(pd.concat(series))
        except ValueError:
            data_flow = pd.DataFrame(pd.Series(name=self.params['codEstacao']))
        return data_flow
