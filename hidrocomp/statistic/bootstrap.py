import pandas as pd


class Bootstrap:

    def __init__(self, data: pd.Series, m: int, name):
        self._sample = None
        self.data = data
        self.n = len(data)
        self.m = m
        self.name = name

    @property
    def sample(self) -> pd.DataFrame:
        if self._sample is None:
            sample = []
            for i in range(self.m):
                sample.append(pd.Series(data=self.data.sample(n=self.n, replace=True).values, name=i+1))
            self._sample = pd.DataFrame(sample).T
        return self._sample

    def mean(self):
        series_mean = self.sample.mean()
        series_mean.name = self.name
        return series_mean

    def std(self):
        return self.sample.std()

    def __str__(self):
        return self.sample.__repr__()

    def __getitem__(self, item):
        return self.sample[item]
