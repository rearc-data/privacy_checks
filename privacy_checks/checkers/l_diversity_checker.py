from pandas import DataFrame
from pycanon import anonymity, report
from .basic_checker import BasicChecker

class LDiversityChecker(BasicChecker):
    def __init__(
        self,
        qi: list,
        sa: list = [],
        l_threshold: int = None,
    ):
        super().__init__('L-Diversity')
        if not isinstance(qi, list):
            raise TypeError("qi must be a list.")
        if not isinstance(sa, list):
            raise TypeError("sa must be a list.")

        # Assign values to instance variables
        self.qi = qi
        self.sa = sa
        self.l_threshold = l_threshold

    def check_dataset(self, df: DataFrame):
        l_div = anonymity.l_diversity(df, self.qi, self.sa)
        if not l_div:
            return {
                'message': 'L-diversity check has failed.',
                'title': 'L-diversity control',
                'status': False,
                'value': 0,
                'threshold': None
            }
        elif self.l_threshold < l_div:
            return {
                'message': 'L-diversity check has failed. Either lower your l threshold or employ techniques to further anonymize this dataset if possible. L-diversity value: {l_div}',
                'title': 'L-diversity control',
                'status': False,
                'value': l_div,
                'threshold': self.l_threshold
            }
        else:
            return {
                'message': 'L-diversity check has passed.',
                'title': 'L-diversity control',
                'status': True,
                'value': l_div,
                'threshold': self.l_threshold
            }