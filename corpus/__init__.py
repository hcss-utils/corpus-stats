import json
import pathlib
import pandas as pd
import pandas.api.types as ptypes


class Corpus:
    
    def __init__(self, path):
        self.path = path
        self.data = None
        self.df = None

    def _load(self):
        p = pathlib.Path(self.path)
        if p.suffix == ".json":
            with open(p, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        elif p.suffix == ".csv":
            self.df = pd.read_csv(p)
        elif p.suffix == ".xlsx":
            self.df = pd.read_excel(p)

    def _to_dataframe(self):
        self.df = pd.json_normalize(self.data)

    def preprocess_data(self):
        self._load()
        if self.df is None:
            self._to_dataframe()
        return self.df.info()
    
    def _check_df(self):
        if self.df is None:
            raise ValueError("Run .preprocess_data() first")

    def view_data(self, sample_size):
        self._check_df()
        return self.df.sample(sample_size)

    def check_formats(self, column):
        self._check_df()
        return self.df[column].value_counts()

    def generate_stats(self, column, dtype="date"):
        self._check_df()
        print(f"total records: {self.df.shape}")
        if dtype == "date":
            s = pd.to_datetime(self.df[column], errors="coerce")
            print(f"Earliest date in the corpus: {s.min()}")
            print(f"Latest date in the corpus: {s.max()}")
            print(f"Missing values: {s.isna().sum()}")
            print("\nDistribution over years: ")
            print(s.dt.year.value_counts())
            return 
        s = self.df[column].astype(str)
        print(f"Min text length: {s.str.len().min()}")
        print(f"Max text length: {s.str.len().max()}")
        print(f"Mean text length: {s.str.len().mean()}")
        print(f"Missing values: {s.isna().sum()}")
        print("\n")
        print(s.describe())
        return 

    def plot_dist(self, column):
        self._check_df()
        s = self.df[column]
        if not ptypes.is_datetime64_dtype(s):
            s = pd.to_datetime(s)
        years = s.dt.year
        table = years.value_counts().to_frame().reset_index()
        table.columns = ["year", "counts"]
        table = table.sort_values("year").reset_index(drop=True)
        return table.plot.bar(x="year", y="counts")
