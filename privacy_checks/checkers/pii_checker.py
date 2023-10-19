import pandas as pd
import json
from dataprofiler import Data, Profiler
from .basic_checker import BasicChecker

class PIIChecker(BasicChecker):
    def __init__(
        self,
        labels: list = [
            "BAN",
            "CREDIT_CARD",
            "EMAIL_ADDRESS",
            "PERSON",
            "DRIVER_LICENSE",
        ],
        detection_threshold: float = 0.5,
    ):
        super().__init__('PII Checker')
        if not isinstance(labels, list):
            raise TypeError("labels must be a list.")
        if not isinstance(detection_threshold, float):
            raise TypeError("detection_threshold must be a float.")

        # Assign values to instance variables
        # self.df = df
        # self.data = Data(data=df, data_type='csv')
        self.profile = None
        self.report = None
        self.detection_threshold = detection_threshold
        self.labels = labels

    def generate_report(self, data):
        # Perform k-anonymity check on the DataFrame
        if (not self.profile):
            self.profile = Profiler(data)
        if (not self.report):
            self.report = self.profile.report(
                report_options={'output_format': 'pretty'})
        return self.report

    def print_metrics(self):
        # Stats for Reporting
        if (not self.report):
            self.generate_report()
        print(f"Data set rows: {self.report['global_stats']['row_count']}")
        for col_data in self.report['data_stats']:
            all_stats = col_data['statistics']
            stats = {
                'unique_ratio': all_stats['unique_ratio'],
                'variance': all_stats['variance'],
                'stddev': all_stats['stddev'],
                'skewness': all_stats['skewness'],
                'kurtosis': all_stats['kurtosis']
            }
            print(f"{col_data['column_name']}: {json.dumps(stats)}")

    def detect_pii_columns(self, df):
        # PII Labels we care about
        data = Data(data=df, data_type='csv')
        if (not self.report):
            self.generate_report(data)

        detected_pii_columns = False
        for col_data in self.report["data_stats"]:
            column_name = col_data["column_name"]
            label_predictions = {
                label: prediction
                for label, prediction in col_data["statistics"][
                    "data_label_representation"
                ].items()
                if prediction > self.detection_threshold and label in self.labels
            }

            if len(label_predictions) > 0:
                print(f"{column_name} predictions: {json.dumps(label_predictions)}")
                detected_pii_columns = True

        if detected_pii_columns:
            # print("Detected unexpected privacy columns!")
            # raise Exception("Detected data columns with potential PII")
            # return (False, 0, 'Detected data columns with potential PII')
            return {
                'message': 'Detected data columns with potential PII.',
                'title': 'PII control',
                'status': False,
                'value': None,
                'threshold': None
            }
        else:
            print("No unexpected privacy columns detected")
            #return (True, 0, 'No unexpected privacy columns detected')
            return {
                'message': 'No columns with PII detected.',
                'title': 'PII control',
                'status': True,
                'value': None,
                'threshold': None
            }

    def check_dataset(self, df):
        return self.detect_pii_columns(df)
