import pandas as pd
from hydrocomp.api_ana.api_biuld import ApiBiuld


class Basin(ApiBiuld):

    url = 'http://telemetriaws1.ana.gov.br/ServiceANA.asmx/HidroBaciaSubBacia'
    params = {'codBacia': '', 'codSubBacia': ''}

    def get(self, **kwargs):
        super().get(**kwargs)

        self.params.update(kwargs)
        root = self.requests()

        basins = pd.DataFrame(columns=['Name_Basin'])
        subbasins = pd.DataFrame(columns=['Name_SubBasin'])

        for basin in root.iter('Table'):
            code_basin = basin.find('codBacia').text
            basins.at[code_basin, 'Name_Basin'] = basin.find('nmBacia').text
            code_subbasin = basin.find('codSubBacia').text
            subbasins.at[code_subbasin, 'Name_SubBasin'] = basin.find('nmSubBacia').text

        return basins, subbasins