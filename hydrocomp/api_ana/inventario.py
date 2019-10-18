import pandas as pd
from hydrocomp.api_ana.api_biuld import ApiBiuld
import geopandas


class Inventario(ApiBiuld):

    url = 'http://telemetriaws1.ana.gov.br/ServiceANA.asmx/HidroInventario'
    params = {'codEstDE': '', 'codEstATE': '', 'tpEst': '', 'nmEst': '', 'nmRio': '', 'codSubBacia': '', 'codBacia': '',
              'nmMunicipio': '', 'nmEstado': '', 'sgResp': '', 'sgOper': '', 'telemetrica': ''}

    def get(self, **kwargs):

        super().get(**kwargs)

        self.params.update(kwargs)
        root = self.requests()

        stations = pd.DataFrame(columns=[
            'Nome', 'Latitude', 'Longitude', 'SubBacia', 'Tipo', 'Municipio',
            'Responsavel', 'Operadora'
        ])
        for station in root.iter('Table'):
            code = station.find('Codigo').text
            stations.at[code, 'Name'] = station.find('Nome').text
            #stations.at[code, 'Point'] = geopandas.points_from_xy(x=float(station.find('Latitude').text), y=[float(station.find('Longitude').text)])
            stations.at[code, 'Latitude'] = float(station.find('Latitude').text)
            stations.at[code, 'Longitude'] = float(station.find('Longitude').text)
            stations.at[code, 'SubBaciaCodigo'] = station.find('SubBaciaCodigo').text
            stations.at[code, 'Tipo'] = station.find('TipoEstacao').text
            stations.at[code, 'MunicipioCodigo'] = station.find('MunicipioCodigo').text
            stations.at[code, 'Responsavel'] = station.find('ResponsavelCodigo').text
            stations.at[code, 'Operadora'] = station.find('OperadoraCodigo').text
            stations.at[code, 'Area'] = station.find('AreaDrenagem').text
        gdf = geopandas.GeoDataFrame(
            stations, geometry=geopandas.points_from_xy(stations.Longitude, stations.Latitude))
        return gdf
