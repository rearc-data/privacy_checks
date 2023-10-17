import pandas as pd
import json
from dataprofiler import Data, Profiler
from basic_checker import BasicChecker

class NullRowChecker(BasicChecker(title='MC Profiler')):
    def __init__(
        self,
        df: pd.DataFrame
    ):
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame.")

        # Assign values to instance variables
        self.df = df
        self.data = Data(data=df, data_type='csv')
        self.profile = None
        self.report = None

    def generate_report(self):
        # Perform k-anonymity check on the DataFrame
        if (not self.profile):
            self.profile = Profiler(self.data)
        if (not self.report):
            self.report = self.profile.report(
                report_options={'output_format': 'pretty'})
        return self.report

    def null_row_check(self):
        if (not self.report):
            self.generate_report()
        null_threshold = 0
        if self.report['global_stats']['row_is_null_ratio'] > null_threshold:
            # print("Null rows found in dataset")
            # raise Exception("Detected null rows within data set")
            return {
                'message': 'Null Row check has failed.',
                'title': 'Null Row control',
                'status': False,
                'value': self.report['global_stats']['row_is_null_ratio'],
                'threshold': null_threshold
            }
        else:
            # print("No null rows found in dataset")
            #return (True, 0, 'No null rows found in dataset')
            return {
                'message': 'No null rows found in dataset.',
                'title': 'Null Row control',
                'status': True,
                'value': self.report['global_stats']['row_is_null_ratio'],
                'threshold': null_threshold
            }
            
    def check_dataset(self):
        return self.null_row_check()