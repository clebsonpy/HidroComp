import pandas as pd
from hidrocomp.statistic.normal import Normal
from hidrocomp.statistic.bootstrap import Bootstrap

from hidrocomp.eflow.graphics import GraphicsDHRAM


class DhramAspect:
    _points = None
    _values = None
    _variables: dict = {}
    _list_name_variables = []

    def __init__(self, name):
        self.aspect_name = name

    @property
    def variables(self):
        return self._variables

    @variables.setter
    def variables(self, variable):
        self._list_name_variables.append(variable.name)
        self._variables[variable.name] = variable

    @property
    def values_mean(self):
        df = pd.DataFrame()
        for i in self._variables:
            df = df.combine_first(self._variables[i].value_mean)
        return df.reindex(self._list_name_variables)

    @property
    def values_std(self):
        df = pd.DataFrame()
        for i in self._variables:
            df = df.combine_first(self._variables[i].value_std)
        return df.reindex(self._list_name_variables)

    @property
    def points(self):
        df = pd.DataFrame()
        for i in self._variables:
            df = df.combine_first(self._variables[i].point)
        return df.reindex(self._list_name_variables)

    @property
    def point(self):
        points = self.points
        df = pd.DataFrame(columns=["Mean", "Std"])
        df.at[self.aspect_name, "Mean"] = points["Mean"].max()
        df.at[self.aspect_name, "Std"] = points["Std"].max()
        return df


class DhramVariable:

    def __init__(self, variable_pre, variable_pos, interval: int, m: int):
        self.name = variable_pre.name
        self.data_pre = variable_pre.data
        self.data_pos = variable_pos.data
        self.interval = interval
        self.sample_pre = Bootstrap(data=self.data_pre, m=m)
        self.sample_pos = Bootstrap(data=self.data_pos, m=m)

    @property
    def value_mean(self):
        value = pd.DataFrame(columns=["Pre - 2_5", "Pre - 97_5", "Pos - 2_5", "Pos - 97_5"])

        dist = Normal(data=list(self.sample_pre.mean().values))
        confidence_intervals_pre = self.sample_pre.mean().quantile([((100 - self.interval) / 2) / 100,
                                                                         1 - ((100 - self.interval) / 2) / 100])
        confidence_intervals_pos = self.sample_pos.mean().quantile([((100 - self.interval) / 2) / 100,
                                                                         1 - ((100 - self.interval) / 2) / 100])

        value.at[self.name, "Pre - 2_5"] = dist.z_score(confidence_intervals_pre[0.025])
        value.at[self.name, "Pre - 97_5"] = dist.z_score(confidence_intervals_pre[0.975])

        value.at[self.name, "Pos - 2_5"] = dist.z_score(confidence_intervals_pos[0.025])
        value.at[self.name, "Pos - 97_5"] = dist.z_score(confidence_intervals_pos[0.975])

        return value

    @property
    def value_std(self):
        value = pd.DataFrame(columns=["Pre - 2_5", "Pre - 97_5", "Pos - 2_5", "Pos - 97_5"])

        dist = Normal(data=list(self.sample_pre.std().values))
        confidence_intervals_pre = self.sample_pre.std().quantile([((100 - self.interval) / 2) / 100,
                                                                    1 - ((100 - self.interval) / 2) / 100])
        confidence_intervals_pos = self.sample_pos.std().quantile([((100 - self.interval) / 2) / 100,
                                                                    1 - ((100 - self.interval) / 2) / 100])

        value.at[self.name, "Pre - 2_5"] = dist.z_score(confidence_intervals_pre[0.025])
        value.at[self.name, "Pre - 97_5"] = dist.z_score(confidence_intervals_pre[0.975])

        value.at[self.name, "Pos - 2_5"] = dist.z_score(confidence_intervals_pos[0.025])
        value.at[self.name, "Pos - 97_5"] = dist.z_score(confidence_intervals_pos[0.975])

        return value

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

    @property
    def point(self) -> pd.DataFrame:
        """
        1 point - 1x z_score(pre)
        2 point - 2x z_score(pre)
        3 point - 3x > z_score(pre)
        @return:
        """
        point_df = pd.DataFrame(columns=["Multi_diff_mean", "Mean", "Multi_diff_std", "Std"])

        z_score_mean = self.value_mean
        z_score_std = self.value_std
        pos_mean_2_5, pos_std_2_5 = z_score_mean["Pos - 2_5"].values[0], z_score_std["Pos - 2_5"].values[0]
        pos_mean_97_5, pos_std_97_5 = z_score_mean["Pos - 97_5"].values[0], z_score_std["Pos - 97_5"].values[0]
        pre_mean_2_5,  pre_std_2_5 = z_score_mean["Pre - 2_5"].values[0], z_score_std["Pre - 2_5"].values[0]
        pre_mean_97_5, pre_std_97_5 = z_score_mean["Pre - 97_5"].values[0], z_score_std["Pre - 97_5"].values[0]

        if abs(pos_mean_2_5) < abs(pos_mean_97_5):
            value_mean_pos = pos_mean_2_5
            diff_mean_pre = abs(value_mean_pos) - abs(pre_mean_2_5)
            multi_diff_mean_pre = diff_mean_pre / 2
        else:
            value_mean_pos = pos_mean_97_5
            diff_mean_pre = abs(value_mean_pos) - abs(pre_mean_97_5)
            multi_diff_mean_pre = diff_mean_pre / 2

        if abs(pos_std_2_5) < abs(pos_std_97_5):
            value_std_pos = pos_std_2_5
            diff_std_pre = abs(value_std_pos) - abs(pre_std_2_5)
            multi_diff_std_pre = diff_std_pre / 2
        else:
            value_std_pos = pos_std_97_5
            diff_std_pre = abs(value_std_pos) - abs(pre_std_97_5)
            multi_diff_std_pre = diff_std_pre / 2

        point_df.at[self.name, "Mean"] = self.__definition_points(multi_diff_mean_pre)
        point_df.at[self.name, "Multi_diff_mean"] = multi_diff_mean_pre * (value_mean_pos/abs(value_mean_pos))
        point_df.at[self.name, "Std"] = self.__definition_points(multi_diff_std_pre)
        point_df.at[self.name, "Multi_diff_std"] = multi_diff_std_pre * (value_std_pos / abs(value_std_pos))

        return point_df

    def plot(self, color={"pre": "blue", "pos": "red"}):
        """
        @type color: dict
        """
        fig_obs, data_obs = GraphicsDHRAM(data_variable=self.sample_pos.mean(), status="pos", color=color).plot()
        fig_nat, data_nat = GraphicsDHRAM(data_variable=self.sample_pre.mean(), status="pre", color=color).plot()

        data = data_obs + data_nat
        fig = dict(data=data, layout=fig_nat['layout'])

        return fig, data

    def __str__(self):
        return self.name
