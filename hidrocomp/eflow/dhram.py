import pandas as pd
from scipy.stats import zscore


class DHRAM:

    def __init__(self, variable_pre, variable_pos, interval: int, n: int):
        self.name_variable = variable_pre.name
        self.data_pre = variable_pre.data
        self.data_pos = variable_pos.data
        self.interval = interval
        self.n = n
        self.sample_pre = self.data_pre.sample(n=self.n, replace=True)
        self.sample_pos = self.data_pos.sample(n=self.n, replace=True)
        self.confidence_intervals_pre = self.sample_pre.quantile([((100 - self.interval) / 2) / 100,
                                                                  1 - ((100 - self.interval) / 2) / 100])
        self.confidence_intervals_pos = self.sample_pos.quantile([((100 - self.interval) / 2) / 100,
                                                                  1 - ((100 - self.interval) / 2) / 100])

    def z_score(self):
        z_score_df = pd.DataFrame(columns=["Pre - 2_5", "Pre - 97_5", "Pos - 2_5", "Pos - 97_5"])

        mean = self.sample_pre.mean()
        std = self.sample_pre.std()

        z_score_df.at[self.name_variable, "Pre - 2_5"] = (self.confidence_intervals_pre[0.025]-mean) / std
        z_score_df.at[self.name_variable, "Pre - 97_5"] = (self.confidence_intervals_pre[0.975]-mean) / std

        z_score_df.at[self.name_variable, "Pos - 2_5"] = (self.confidence_intervals_pos[0.025] - mean) / std
        z_score_df.at[self.name_variable, "Pos - 97_5"] = (self.confidence_intervals_pos[0.975] - mean) / std

        return z_score_df
