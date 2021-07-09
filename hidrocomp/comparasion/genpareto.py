from scipy.stats import genpareto
import pandas as pd

from hidrocomp.comparasion.bootstrap_build import BootstrapBuild


class BootsGenPareto(BootstrapBuild):

    def __init__(self, shape, location, scale, size):
        super().__init__(shape, location, scale, size)

    def fit_resample(self):
        resample = genpareto.rvs(self.shape, self.location, self.scale,
                                 self.size)
        return genpareto.fit(resample)

    def fits_resamples(self, quantity):
        list_fits = list()
        for i in range(quantity):
            list_fits.append(self.fit_resample())

        return list_fits

    def magnitudes_resamples(self, quantity):
        dic_magns = {0.001: list(), 0.01: list(), 0.1: list(),
                     0.5: list(), 0.9: list(), 0.99: list(), 0.999: list()
                     }
        for i in range(quantity):
            fit = self.fit_resample()
            for j in dic_magns:
                mag = genpareto.ppf(j, fit[0], fit[1], fit[2])
                dic_magns[j].append(mag)

        return pd.DataFrame(dic_magns)
