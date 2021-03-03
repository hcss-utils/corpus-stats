import json
import pandas as pd


class Corpus:
 
    def __init__(self, path):
        self.path = path
        self.data = None
        self.df = None
        self.fig = None

    def _load(self):
        pass

    def _to_dataframe(self):
        pass

    def preprocess_data(self):
        pass

    def check_formats(self, column):
        pass

    def check_nans(self, column):
        pass

    def generate_stats():
        pass

    def plot_dist():
        pass
