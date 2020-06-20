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
    def diff(self):
        df = pd.DataFrame()
        for i in self._variables:
            df = df.combine_first(self._variables[i].diff)
        return df.reindex(self._list_name_variables)

    @property
    def point(self):
        diff_mean = self.diff.abs().mean()
        print(diff_mean)
        df = pd.DataFrame(columns=["Mean", "Std"])
        df.at[self.aspect_name, "Mean"] = self.__definition_points(diff_mean["Multi_diff_mean"])
        df.at[self.aspect_name, "Std"] = self.__definition_points(diff_mean["Multi_diff_std"])
        return df

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


class DhramVariable:

    def __init__(self, variable_pre, variable_pos, interval: int, m: int):
        self.name = variable_pre.name
        self.data_pre = variable_pre.data
        self.data_pos = variable_pos.data
        self.interval = [((100 - interval) / 2) / 100, 1 - ((100 - interval) / 2) / 100]
        self.sample_pre = Bootstrap(data=self.data_pre, m=m)
        self.sample_pos = Bootstrap(data=self.data_pos, m=m)

    def __calc_value(self, dist_pre, dist_pos):
        value = pd.DataFrame(columns=["Pre - 2_5", "Pre - 97_5", "Pos - 2_5", "Pos - 97_5"])
        confidence_intervals_pre = dist_pre.data.quantile(self.interval)
        confidence_intervals_pos = dist_pos.data.quantile(self.interval)

        value.at[self.name, "Pre - 2_5"] = dist_pre.z_score(confidence_intervals_pre[0.025])
        value.at[self.name, "Pre - 97_5"] = dist_pre.z_score(confidence_intervals_pre[0.975])

        value.at[self.name, "Pos - 2_5"] = dist_pre.z_score(confidence_intervals_pos[0.025])
        value.at[self.name, "Pos - 97_5"] = dist_pre.z_score(confidence_intervals_pos[0.975])
        return value

    @property
    def value_mean(self):

        dist_pre = Normal(data=self.sample_pre.mean())
        dist_pos = Normal(data=self.sample_pos.mean())

        value = self.__calc_value(dist_pre=dist_pre, dist_pos=dist_pos)

        return value

    @property
    def value_std(self):

        dist_pre = Normal(data=self.sample_pre.std())
        dist_pos = Normal(data=self.sample_pos.std())

        value = self.__calc_value(dist_pre=dist_pre, dist_pos=dist_pos)

        return value

    @staticmethod
    def __calc_diff(pre_2_5, pre_97_5, pos_2_5, pos_97_5):
        if abs(pos_2_5) < abs(pos_97_5):
            value_pos = pos_2_5
            diff_pre = abs(value_pos) - abs(pre_2_5)
            multi_diff_pre = diff_pre / 2
        else:
            value_pos = pos_97_5
            diff_pre = abs(value_pos) - abs(pre_97_5)
            multi_diff_pre = diff_pre / 2

        return multi_diff_pre, value_pos

    @property
    def diff(self) -> pd.DataFrame:

        diff_df = pd.DataFrame(columns=["Multi_diff_mean", "Multi_diff_std"])

        z_score_mean = self.value_mean
        z_score_std = self.value_std
        pos_mean_2_5, pos_std_2_5 = z_score_mean["Pos - 2_5"].values[0], z_score_std["Pos - 2_5"].values[0]
        pos_mean_97_5, pos_std_97_5 = z_score_mean["Pos - 97_5"].values[0], z_score_std["Pos - 97_5"].values[0]
        pre_mean_2_5,  pre_std_2_5 = z_score_mean["Pre - 2_5"].values[0], z_score_std["Pre - 2_5"].values[0]
        pre_mean_97_5, pre_std_97_5 = z_score_mean["Pre - 97_5"].values[0], z_score_std["Pre - 97_5"].values[0]

        multi_diff_mean_pre, value_mean_pos = self.__calc_diff(pre_mean_2_5, pre_mean_97_5, pos_mean_2_5, pos_mean_97_5)
        multi_diff_std_pre, value_std_pos = self.__calc_diff(pre_std_2_5, pre_std_97_5, pos_std_2_5, pos_std_97_5)

        diff_df.at[self.name, "Multi_diff_mean"] = multi_diff_mean_pre * (value_mean_pos/abs(value_mean_pos))
        diff_df.at[self.name, "Multi_diff_std"] = multi_diff_std_pre * (value_std_pos / abs(value_std_pos))

        return diff_df

    def plot(self, color={"pre": "blue", "pos": "red"}, type="mean"):
        """
        @type color: dict
        """
        if type == "mean":
            fig_obs, data_obs = GraphicsDHRAM(data_variable=self.sample_pos.mean(), status="pos", color=color,
                                              name=self.name).plot()
            fig_nat, data_nat = GraphicsDHRAM(data_variable=self.sample_pre.mean(), status="pre", color=color,
                                              name=self.name).plot()
        elif type == "std":
            fig_obs, data_obs = GraphicsDHRAM(data_variable=self.sample_pos.std(), status="pos", color=color,
                                              name=self.name).plot()
            fig_nat, data_nat = GraphicsDHRAM(data_variable=self.sample_pre.std(), status="pre", color=color,
                                              name=self.name).plot()
        else:
            raise AttributeError("Type Error")

        data = data_obs + data_nat
        fig = dict(data=data, layout=fig_nat['layout'])

        return fig, data

    def __str__(self):
        return self.name
