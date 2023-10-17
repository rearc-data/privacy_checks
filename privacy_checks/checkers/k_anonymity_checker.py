from pandas import DataFrame
from pycanon import anonymity, report
from basic_checker import BasicChecker


class KAnonymityChecker(BasicChecker(title='K-Anonymity')):
    def __init__(
        self,
        qi: list,
        k_threshold: int = None,
    ):
        if not isinstance(qi, list):
            raise TypeError("qi must be a list.")

        # Assign values to instance variables
        self.qi = qi
        self.sa = sa
        self.k_threshold = k_threshold

    def check_dataset(self, df: DataFrame):
        # Perform k-anonymity check on the DataFrame
        k = anonymity.k_anonymity(df, self.qi)
        if k < self.k_threshold:
            return {
                'message': 'K-anonymity check has failed.  Either lower your k threshold or employ techniques to further anonymize this dataset if possible.',
                'title': 'K-anonymity control',
                'status': False,
                'value': k,
                'threshold': self.k_threshold
            }
        else:
            return {
                'message': 'K-anonymity check has passed.',
                'title': 'K-anonymity control',
                'status': True,
                'value': k,
                'threshold': self.k_threshold
            }

    
