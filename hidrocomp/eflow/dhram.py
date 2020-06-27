import pandas as pd
from hidrocomp.statistic.normal import Normal
from hidrocomp.statistic.bootstrap import Bootstrap
from hidrocomp.eflow.exceptions import *
from hidrocomp.eflow.graphics import GraphicsDHRAM


class Dhram:

    def __init__(self):
        self._point = None
        self._aspects: dict = {}
        self._classification = None

    @property
    def aspects(self):
        return self._aspects

    @aspects.setter
    def aspects(self, aspect):
        self._aspects[aspect.name] = aspect

    @property
    def point(self):
        if self._point is None:
            df = pd.DataFrame()
            for i in self.aspects:
                df = df.combine_first(self.aspects[i].point)
            self._point = df
        return self._point

    @staticmethod
    def __definition_classification(points) -> str:
        if points == 0:
            return "{} Points - Un-impacted".format(points)
        elif 1 <= points <= 4:
            return "{} Points - Low risk of impact".format(points)
        elif 5 <= points <= 10:
            return "{} Points - Moderate risk of impact".format(points)
        elif 11 <= points <= 20:
            return "{} Points - High risk of impact".format(points)
        elif 21 <= points <= 30:
            return "{} Points - Severely impacted".format(points)

    @property
    def classification(self):
        points = self.point.sum().sum()
        if self._classification is None:
            self._classification = self.__definition_classification(points=points)
        return self._classification


class DhramAspect:

    def __init__(self, name):
        self.name = name
        self._point = None
        self._variables: dict = {}
        self._list_name_variables = []

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
        for i in self.variables:
            df = df.combine_first(self.variables[i].value_mean)
        return df.reindex(self._list_name_variables)

    @property
    def values_std(self):
        df = pd.DataFrame()
        for i in self.variables:
            df = df.combine_first(self.variables[i].value_std)
        return df.reindex(self._list_name_variables)

    @property
    def abnormality(self):
        if self._point is None:
            df = pd.DataFrame()
            for i in self.variables:
                df = df.combine_first(self.variables[i].abnormality)
            self._point = df.reindex(self._list_name_variables)
        return self._point

    @property
    def point(self):
        diff_mean = self.abnormality.abs().mean()
        df = pd.DataFrame(columns=["Mean", "Std"])
        df.at[self.name, "Mean"] = self.__definition_points(diff_mean["Abnormality_mean"])
        df.at[self.name, "Std"] = self.__definition_points(diff_mean["Abnormality_std"])
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

    def plot(self, data_type="mean"):
        graphs = GraphicsDHRAM(obj_dhram=self, data_type=data_type, xaxis="Variable", yaxis="Data")
        fig, data = graphs.plot(type="error_bar")
        return fig, data


class DhramVariable:

    def __init__(self, variable_pre, variable_pos, interval: int, m: int):
        self.name = variable_pre.name
        self.data_pre = variable_pre.data
        self.data_pos = variable_pos.data
        self.interval = [((100 - interval) / 2) / 100, 1 - ((100 - interval) / 2) / 100]
        self.sample_pre = Bootstrap(data=self.data_pre, m=m, name=self.name)
        self.sample_pos = Bootstrap(data=self.data_pos, m=m, name=self.name)

    def __calc_value(self, dist_pre, dist_pos):
        value = pd.DataFrame(columns=["Pre - 2_5", "Pre - 97_5", "Pos - 2_5", "Pos - 97_5"])
        confidence_intervals_pre = dist_pre.data.quantile(self.interval)
        confidence_intervals_pos = dist_pos.data.quantile(self.interval)

        value.at[self.name, "Pre - 2_5"] = dist_pre.z_score(confidence_intervals_pre[self.interval[0]])
        value.at[self.name, "Pre - 97_5"] = dist_pre.z_score(confidence_intervals_pre[self.interval[1]])

        value.at[self.name, "Pos - 2_5"] = dist_pre.z_score(confidence_intervals_pos[self.interval[0]])
        value.at[self.name, "Pos - 97_5"] = dist_pre.z_score(confidence_intervals_pos[self.interval[0]])
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
    def abnormality(self) -> pd.DataFrame:

        diff_df = pd.DataFrame(columns=["Abnormality_mean", "Abnormality_std"])

        z_score_mean = self.value_mean
        z_score_std = self.value_std
        pos_mean_2_5, pos_std_2_5 = z_score_mean["Pos - 2_5"].values[0], z_score_std["Pos - 2_5"].values[0]
        pos_mean_97_5, pos_std_97_5 = z_score_mean["Pos - 97_5"].values[0], z_score_std["Pos - 97_5"].values[0]
        pre_mean_2_5,  pre_std_2_5 = z_score_mean["Pre - 2_5"].values[0], z_score_std["Pre - 2_5"].values[0]
        pre_mean_97_5, pre_std_97_5 = z_score_mean["Pre - 97_5"].values[0], z_score_std["Pre - 97_5"].values[0]

        multi_diff_mean_pre, value_mean_pos = self.__calc_diff(pre_mean_2_5, pre_mean_97_5, pos_mean_2_5, pos_mean_97_5)
        multi_diff_std_pre, value_std_pos = self.__calc_diff(pre_std_2_5, pre_std_97_5, pos_std_2_5, pos_std_97_5)

        diff_df.at[self.name, "Abnormality_mean"] = multi_diff_mean_pre * (value_mean_pos/abs(value_mean_pos))
        diff_df.at[self.name, "Abnormality_std"] = multi_diff_std_pre * (value_std_pos / abs(value_std_pos))

        return diff_df

    def plot(self, color={"pre": "blue", "pos": "red"}, type="mean"):
        """
        @type color: dict
        """
        if type == "mean":
            fig_obs, data_obs = GraphicsDHRAM(obj_dhram=self, color=color, name=self.name).plot(type="point")
            fig_nat, data_nat = GraphicsDHRAM(obj_dhram=self, color=color, name=self.name).plot(type="point")
        elif type == "std":
            fig_obs, data_obs = GraphicsDHRAM(obj_dhram=self, color=color, name=self.name).plot(type="point")
            fig_nat, data_nat = GraphicsDHRAM(obj_dhram=self, color=color, name=self.name).plot(type="point")
        else:
            raise AttributeError("Type Error")

        data = data_obs + data_nat
        fig = dict(data=data, layout=fig_nat['layout'])

        return fig, data

    def __str__(self):
        return self.name
