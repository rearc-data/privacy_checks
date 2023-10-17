from pandas import DataFrame
from pycanon import anonymity, report
from .basic_checker import BasicChecker

class TClosenessChecker(BasicChecker):
    def __init__(
        self,
        qi: list,
        sa: list = [],
        t_threshold: float = None,
    ):
        super().__init__('T-Closeness')
        if not isinstance(qi, list):
            raise TypeError("qi must be a list.")
        if not isinstance(sa, list):
            raise TypeError("sa must be a list.")

        # Assign values to instance variables
        self.qi = qi
        self.sa = sa
        self.t_threshold = t_threshold

    def check_dataset(self, df: DataFrame):
        t_closeness = anonymity.t_closeness(df, self.qi, self.sa)
        print(t_closeness)
        if not t_closeness:
            return {
                'message': 'T-Closeness check has failed.',
                'title': 'T-Closeness control',
                'status': False,
                'value': 0,
                'threshold': None
            }
        elif self.t_threshold < t_closeness:
            return {
                'message': 'T-Closeness check has failed. Either lower your t threshold or employ techniques to further anonymize this dataset if possible. T-Closeness value: {t_closeness}',
                'title': 'T-Closeness control',
                'status': False,
                'value': t_closeness,
                'threshold': self.t_threshold
            }
        else:
            return {
                'message': 'T-Closeness check has passed.',
                'title': 'T-Closeness control',
                'status': True,
                'value': t_closeness,
                'threshold': self.t_threshold
            }