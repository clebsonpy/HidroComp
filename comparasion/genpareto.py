from scipy.stats import genpareto
import pandas as pd

from comparasion.bootstrap_build import BootstrapBuild


class BootsGenPareto(BootstrapBuild):

    def __init__(self, forma, localizacao, escala, tamanho):
         super().__init__(forma, localizacao, escala, tamanho)

    def fit_resample(self):
        resample = genpareto.rvs(self.forma, self.localizacao, self.escala,
                                     self.tamanho)
        return genpareto.fit(resample)

    def fits_resamples(self, quantidade):
        list_fits = []
        for i in range(quantidade):
            list_fits.append(self.fit_resample())

        return list_fits

    def magnitudes_resamples(self, quantidade):
        dic_magns = {0.001:[], 0.01:[], 0.1:[], 0.5:[], 0.9:[], 0.99:[], 0.999:[]}
        for i in range(quantidade):
            fit = self.fit_resample()
            for j in dic_magns:
                mag = genpareto.ppf(j, fit[0], fit[1], fit[2])
                dic_magns[j].append(mag)

        return pd.DataFrame(dic_magns)
