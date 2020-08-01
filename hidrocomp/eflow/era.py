import pandas as pd
import plotly.graph_objs as go
from hidrocomp.statistic.normal import Normal
from hidrocomp.statistic.bootstrap import Bootstrap
from hidrocomp.eflow.exceptions import *
from hidrocomp.eflow.graphics import GraphicsCha


class Era:

    def __init__(self):
        self._point = None
        self._aspects: dict = {}
        self._classification = None
        self._abnormality = None

    @property
    def aspects(self):
        return self._aspects

    @aspects.setter
    def aspects(self, aspect):
        self._aspects[aspect.name] = aspect

    def values_mean(self):
        df = pd.DataFrame()
        for aspect in self.aspects:
            df = df.combine_first(self.aspects[aspect].values_mean)
        return df["Pos - mean"]

    def values_std(self):
        df = pd.DataFrame()
        for aspect in self.aspects:
            df = df.combine_first(self.aspects[aspect].values_std)
        return df["Pos - mean"]

    @property
    def abnormality(self):
        if self._abnormality is None:
            df = pd.DataFrame()
            for aspect in self.aspects:
                df = df.combine_first(self.aspects[aspect].abnormality)
            self._abnormality = df
            return self._abnormality
        return self._abnormality

    def plot(self, data_type="diff", by_type_events=None, showlegend: bool = False, size_text: int =14,
             names_variables: dict = None):
        data_type_dict = {'std': "Standard deviation", "mean": "Mean"}
        data = []

        symbol = {"1-day maximum": 'circle', "Date of maximum": 'x', "High events count": 'triangle-up',
                  "High events duration": 'cross', "1-day minimum": 'circle', "Date of minimum": 'x',
                  "Low events count": 'triangle-up', "Low events duration": 'cross'}

        names = {"1-day maximum": "Magnitude", "Date of maximum": "Timing", "High events count": "Frequency",
                 "High events duration": "Duration", "1-day minimum": "Magnitude", "Date of minimum": "Timing",
                 "Low events count": "Frequency", "Low events duration": "Duration"}

        x = []
        error = []
        error_minus = []
        for i in self.aspects:
            for j in self.aspects[i].variables:
                graphs = GraphicsCha(obj_dhram=self.aspects[i].variables[j], data_type=data_type, xaxis="Variables",
                                     yaxis="Z-scores", size_text=size_text, names_variables=names_variables)
                try:
                    fig, df = graphs.plot(type="error_bar", by_type_events=by_type_events)
                except TypeError:
                    continue
                data_fig = fig["data"]
                error = error + list(df["Data"].values + df["Error"].values)
                error_minus = error_minus + list(df["Data"].values - df["Error_minus"].values)
                x = x + list(df["Variable"].values)
                data_fig[0]["name"] = names[j]
                data_fig[0]["marker"]["color"] = "black"
                data_fig[0]["marker"]["symbol"] = symbol[j]
                data_fig[0]["showlegend"] = False

                data_fig[1]["name"] = names[j]
                data_fig[1]["marker"]["color"] = "black"
                data_fig[1]["marker"]["symbol"] = symbol[j]
                data = data + [data_fig[0], data_fig[1]]
        layout = fig["layout"]
        layout['showlegend'] = showlegend
        layout["title"]["text"] = None
        fig = go.Figure(data=data, layout=layout)
        fig.add_trace(go.Scatter(
            x=x, y=[2] * len(x),
            mode='lines',
            line=dict(width=0.5, color='#2EFE2E'),
            stackgroup="one",
            showlegend=False,
        ))
        fig.add_trace(go.Scatter(
            x=x, y=[2] * len(x),
            mode='lines',
            line=dict(width=0.5, color='#F7FE2E'),
            stackgroup="one",
            showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=x, y=[2] * len(x),
            mode='lines',
            line=dict(width=0.5, color='#FAAC58'),
            stackgroup="one",
            showlegend=False
        ))
        if max(error) > 6:
            fig.add_trace(go.Scatter(
                x=x, y=[max(error) - 6] * len(x),
                mode='lines',
                line=dict(width=0.5, color='#FE2E2E'),
                stackgroup="one",
                showlegend=False
            ))
        fig.add_trace(go.Scatter(
            x=x, y=[-2] * len(x),
            mode='lines',
            line=dict(width=0.5, color='#2EFE2E'),
            stackgroup="two",
            showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=x, y=[-2] * len(x),
            mode='lines',
            line=dict(width=0.5, color='#F7FE2E'),
            stackgroup="two",
            showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=x, y=[-2] * len(x),
            mode='lines',
            line=dict(width=0.5, color='#FAAC58'),
            stackgroup="two",
            showlegend=False
        ))
        error_minus_not_null = [x for x in error_minus if str(x) != 'nan']
        if min(error_minus_not_null) < -6:
            fig.add_trace(go.Scatter(
                x=x, y=[min(error_minus_not_null)+6] * len(x),
                mode='lines',
                line=dict(width=0.5, color='#FE2E2E'),
                stackgroup="two",
                showlegend=False
            ))
        return fig, data


class EraAspect:

    def __init__(self, name):
        self.name = name
        self._abnormality = None
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
        if self._abnormality is None:
            df = pd.DataFrame()
            for i in self.variables:
                df = df.combine_first(self.variables[i].abnormality)
            self._abnormality = df.reindex(self._list_name_variables)

        return self._abnormality

    def plot(self, data_type="mean"):
        graphs = GraphicsCha(obj_dhram=self, data_type=data_type, xaxis="Variable", yaxis="Abnormality")
        fig, data = graphs.plot(type="error_bar")
        return fig, data


class EraVariable:

    def __init__(self, variable_pre, variable_pos, interval: int, m: int):
        self.name = variable_pre.name
        self.data_pre = variable_pre.data
        self.data_pos = variable_pos.data
        self.data_pos_nulls = self.data_pos
        self.interval = [((100 - interval) / 2) / 100, 1 - ((100 - interval) / 2) / 100]
        self.sample_pre = Bootstrap(data=self.data_pre, m=m, name=self.name)
        self.sample_pos = Bootstrap(data=self.data_pos, m=m, name=self.name)
        self.sample_diff = Bootstrap(data=self.data_pre-self.data_pos, m=m, name=self.name)

    def __calc_value(self, dist_pre, dist_pos, dist_diff):
        value = pd.DataFrame(columns=["Pre - 2_5", "Pre - 97_5", "Pos - 2_5", "Pos - 97_5", "Pre - mean", "Pos - mean"],
                             dtype='float64')
        confidence_intervals_pre = dist_pre.data.quantile(self.interval)
        confidence_intervals_pos = dist_pos.data.quantile(self.interval)
        confidence_intervals_diff = dist_diff.data.quantile(self.interval)
        zscore_pre_2_5 = dist_pre.z_score(confidence_intervals_pre[self.interval[0]])
        zscore_pos_2_5 = dist_pre.z_score(confidence_intervals_pos[self.interval[0]])
        zscore_pre_97_5 = dist_pre.z_score(confidence_intervals_pre[self.interval[1]])
        zscore_pos_97_5 = dist_pre.z_score(confidence_intervals_pos[self.interval[1]])
        zscore_pre_mean = dist_pre.z_score(dist_pre.data.mean())
        zscore_pos_mean = dist_pre.z_score(dist_pos.data.mean())

        value.at[self.name, "Pre - 2_5"] = zscore_pre_2_5
        value.at[self.name, "Pre - mean"] = zscore_pre_mean
        value.at[self.name, "Pre - 97_5"] = zscore_pre_97_5

        value.at[self.name, "Pos - 2_5"] = zscore_pos_2_5
        value.at[self.name, "Pos - mean"] = zscore_pos_mean
        value.at[self.name, "Pos - 97_5"] = zscore_pos_97_5
        return value

    @property
    def value_mean(self):

        dist_pre = Normal(data=self.sample_pre.mean())
        dist_pos = Normal(data=self.sample_pos.mean())
        dist_diff = Normal(data=self.sample_diff.mean())

        value = self.__calc_value(dist_pre=dist_pre, dist_pos=dist_pos, dist_diff=dist_diff)
        return value

    @property
    def value_std(self):

        dist_pre = Normal(data=self.sample_pre.std())
        dist_pos = Normal(data=self.sample_pos.std())
        dist_diff = Normal(data=self.sample_diff.std())

        value = self.__calc_value(dist_pre=dist_pre, dist_pos=dist_pos, dist_diff=dist_diff)

        return value

    @staticmethod
    def __calc_abnormality(pos_2_5, pos_97_5):
        if abs(pos_2_5) < abs(pos_97_5):
            value_pos = pos_2_5
        else:
            value_pos = pos_97_5

        multi_diff = (abs(abs(value_pos) - 2) / 2) * value_pos/abs(value_pos)
        return multi_diff

    @property
    def abnormality(self) -> pd.DataFrame:

        diff_df = pd.DataFrame(columns=["Abnormality_mean", "Abnormality_std"])

        z_score_mean = self.value_mean
        z_score_std = self.value_std
        pos_mean_2_5, pos_std_2_5 = z_score_mean["Pos - 2_5"].values[0], z_score_std["Pos - 2_5"].values[0]
        pos_mean_97_5, pos_std_97_5 = z_score_mean["Pos - 97_5"].values[0], z_score_std["Pos - 97_5"].values[0]

        value_mean_pos = self.__calc_abnormality(pos_mean_2_5, pos_mean_97_5)
        value_std_pos = self.__calc_abnormality(pos_std_2_5, pos_std_97_5)

        diff_df.at[self.name, "Abnormality_mean"] = value_mean_pos
        diff_df.at[self.name, "Abnormality_std"] = value_std_pos

        return diff_df

    def plot(self, color={"pre": "blue", "pos": "red"}, type="mean"):
        """
        @type color: dict
        """
        if type == "mean":
            fig_obs, data_obs = GraphicsCha(obj_dhram=self, color=color, name=self.name).plot(type="point")
            fig_nat, data_nat = GraphicsCha(obj_dhram=self, color=color, name=self.name).plot(type="point")
        elif type == "std":
            fig_obs, data_obs = GraphicsCha(obj_dhram=self, color=color, name=self.name).plot(type="point")
            fig_nat, data_nat = GraphicsCha(obj_dhram=self, color=color, name=self.name).plot(type="point")
        else:
            raise AttributeError("Type Error")

        data = data_obs + data_nat
        fig = dict(data=data, layout=fig_nat['layout'])

        return fig, data

    def __str__(self):
        return self.name
