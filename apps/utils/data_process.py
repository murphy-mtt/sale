import pandas as pd
from django.apps import apps


class Chandler:
    def __init__(self):
        pass


class DataStorage(Chandler):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def read_file(self):
        return pd.read_excel(self.file_path, sheet_name='Sheet1')
