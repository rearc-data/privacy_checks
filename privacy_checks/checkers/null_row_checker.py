import pandas as pd
from .basic_checker import BasicChecker

class NullRowChecker(BasicChecker):
    def __init__(
        self
    ):
        super().__init__('Null Row Checker')
            
    def check_dataset(self, df):
        null_rows = df.isnull().all(axis=1)
        null_row_count = null_rows.sum()
        if null_rows.any():
            return {
                'message': 'Null Row check has failed.',
                'title': 'Null Row control',
                'status': False,
                'value': null_row_count,
                'threshold': 0
            }
        else:
            return {
                'message': 'No null rows found in dataset.',
                'title': 'Null Row control',
                'status': True,
                'value': null_row_count,
                'threshold': 0
            }
