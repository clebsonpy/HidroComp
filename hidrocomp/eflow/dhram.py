import pandas as pd
from hidrocomp.statistic.normal import Normal

from hidrocomp.eflow.graphics import GraphicsDHRAM


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

    def value(self):
        z_score_df = pd.DataFrame(columns=["Pre - 2_5", "Pre - 97_5", "Pos - 2_5", "Pos - 97_5"])

        dist = Normal(data=list(self.sample_mean_pre.values))

        z_score_df.at[self.name_variable, "Pre - 2_5"] = dist.z_score(self.confidence_intervals_pre[0.025])
        z_score_df.at[self.name_variable, "Pre - 97_5"] = dist.z_score(self.confidence_intervals_pre[0.975])

        z_score_df.at[self.name_variable, "Pos - 2_5"] = dist.z_score(self.confidence_intervals_pos[0.025])
        z_score_df.at[self.name_variable, "Pos - 97_5"] = dist.z_score(self.confidence_intervals_pos[0.975])

        return z_score_df

    @staticmethod
    def __definition_points(multi_pre):
        if 1 < multi_pre <= 2:
            return 1
        elif 2 < multi_pre <= 3:
            return 2
        elif multi_pre > 3:
            return 3
        else:
            return 0

    def points(self):
        """
        1 point - 1x z_score(pre)
        2 point - 2x z_score(pre)
        3 point - 3x > z_score(pre)
        @return:
        """
        point_df = pd.DataFrame(columns=["Diff", "Point"])

        z_score = self.value()
        pos_2_5 = z_score["Pos - 2_5"].values[0]
        pos_97_5 = z_score["Pos - 97_5"].values[0]
        pre_2_5 = z_score["Pre - 2_5"].values[0]
        pre_97_5 = z_score["Pre - 97_5"].values[0]

        if abs(pos_2_5) < abs(pos_97_5):
            value_pos = pos_2_5
        else:
            value_pos = pos_97_5

        if value_pos < 0:
            multi_pre = value_pos / pre_2_5
        else:
            multi_pre = value_pos / pre_97_5

        point_df.at[self.name_variable, "Point"] = self.__definition_points(multi_pre)
        point_df.at[self.name_variable, "Diff"] = multi_pre

        return point_df

    def plot(self, color={"pre": "blue", "pos": "red"}):
        """
        @type color: dict
        """
        fig_obs, data_obs = GraphicsDHRAM(data_variable=self.sample_mean_pos, status="pos", color=color,
                                          interval_confidence=self.confidence_intervals_pos).plot()
        fig_nat, data_nat = GraphicsDHRAM(data_variable=self.sample_mean_pre, status="pre", color=color,
                                          interval_confidence=self.confidence_intervals_pre).plot()

        data = data_obs + data_nat
        fig = dict(data=data, layout=fig_nat['layout'])

        return fig, data
