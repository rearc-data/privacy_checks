import pandas as pd
from dataprofiler import Data, Profiler

class Profiler:
    def __init__(
        self,
        df: pd.DataFrame,
        labels: list = [
            "BAN",
            "CREDIT_CARD",
            "EMAIL_ADDRESS",
            "PERSON",
            "DRIVER_LICENSE",
        ],
        detection_threshold: float = 0.5,
    ):
        if not isinstance(labels, list):
            raise TypeError("labels must be a list.")
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame.")
        if not isinstance(detection_threshold, float):
            raise TypeError("detection_threshold must be a list.")
        
        # Assign values to instance variables
        self.qi = qi
        self.df = df
        self.sa = sa
        self.data = Data(df, data_type='csv')
        self.profile = None
        self.report = None

    def generate_report(self):
        # Perform k-anonymity check on the DataFrame
        if(not self.profile):
            self.profile = Profiler(self.data)
        if(not self.report):
            self.report = self.profile.report(report_options={'output_format':'pretty'})
        return self.report

    def null_row_check(self):
        if(not self.report):
            self.generate_report()
        null_threshold = 0
        if self.report['global_stats']['row_is_null_ratio'] > null_threshold:
            print("Null rows found in dataset")
            raise Exception("Detected null rows within data set")
        else:
            print("No null rows found in dataset")
            return True
    
    def print_metrics(self):
        # Stats for Reporting
        if(not self.report):
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
    
    def detect_pii_columns(self):
        # PII Labels we care about
        if(not self.report):
            self.generate_report()


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
            print("Detected unexpected privacy columns!")
            raise Exception("Detected data columns with potential PII")
        else:
            print("No unexpected privacy columns detected")
            return True