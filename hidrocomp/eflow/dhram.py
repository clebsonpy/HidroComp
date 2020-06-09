import pandas as pd
from scipy.stats import zscore


class DHRAM:

    def __init__(self, variable_pre, variable_pos, interval: int, m: int):
        self.name_variable = variable_pre.name
        self.data_pre = variable_pre.data
        self.data_pos = variable_pos.data
        self.interval = interval
        self.n_pre = len(self.data_pre)
        self.n_pos = len(self.data_pos)
        self.sample_mean_pre = pd.Series(data=[self.data_pre.sample(n=self.n_pre, replace=True).mean()
                                               for _ in range(m)], name=self.name_variable)
        self.sample_mean_pos = pd.Series(data=[self.data_pos.sample(n=self.n_pos, replace=True).mean()
                                               for _ in range(m)], name=self.name_variable)
        self.confidence_intervals_pre = self.sample_mean_pre.quantile([((100 - self.interval) / 2) / 100,
                                                                       1 - ((100 - self.interval) / 2) / 100])
        self.confidence_intervals_pos = self.sample_mean_pos.quantile([((100 - self.interval) / 2) / 100,
                                                                       1 - ((100 - self.interval) / 2) / 100])

    def z_score(self):
        z_score_df = pd.DataFrame(columns=["Pre - 2_5", "Pre - 97_5", "Pos - 2_5", "Pos - 97_5"])

        mean = self.sample_mean_pre.mean()
        std = self.sample_mean_pre.std()

        z_score_df.at[self.name_variable, "Pre - 2_5"] = (self.confidence_intervals_pre[0.025] - mean) / std
        z_score_df.at[self.name_variable, "Pre - 97_5"] = (self.confidence_intervals_pre[0.975] - mean) / std

        z_score_df.at[self.name_variable, "Pos - 2_5"] = (self.confidence_intervals_pos[0.025] - mean) / std
        z_score_df.at[self.name_variable, "Pos - 97_5"] = (self.confidence_intervals_pos[0.975] - mean) / std

        return z_score_df
