from pandas import DataFrame
from pycanon import anonymity, report
from .basic_checker import BasicChecker

class CLDiversityChecker(BasicChecker):
    def __init__(
        self,
        qi: list,
        sa: list = [],
        c_threshold: float = None,
    ):
        super().__init__('(C, L)-Diversity')
        if not isinstance(qi, list):
            raise TypeError("qi must be a list.")
        if not isinstance(sa, list):
            raise TypeError("sa must be a list.")

        # Assign values to instance variables
        self.qi = qi
        self.sa = sa
        self.c_threshold = c_threshold

    def check_dataset(self, df: DataFrame):
        c_l_div = anonymity.recursive_c_l_diversity(df, self.qi, self.sa)[0]
        if not c_l_div:
            return {
                'message': '(C, L)-diversity check has failed.',
                'title': '(C, L)-diversity control',
                'status': False,
                'value': 0,
                'threshold': None
            }
        elif self.c_threshold < c_l_div:
            return {
                'message': '(C, L)-diversity check has failed. Either lower your C threshold or employ techniques to further anonymize this dataset if possible. (C, L)-diversity value: {c_l_div}',
                'title': '(C, L)-diversity control',
                'status': False,
                'value': c_l_div,
                'threshold': self.c_threshold
            }
        else:
            return {
                'message': '(C, L)-diversity check has passed.',
                'title': '(C, L)-diversity control',
                'status': True,
                'value': c_l_div,
                'threshold': self.c_threshold
            }