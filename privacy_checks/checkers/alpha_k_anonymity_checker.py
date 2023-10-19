from pandas import DataFrame
from pycanon import anonymity, report
from .basic_checker import BasicChecker

class AlphaKAnonymityChecker(BasicChecker):
    def __init__(
        self,
        qi: list,
        sa: list = [],
        alpha_threshold: float = None,
    ):
        super().__init__('(Alpha, K)-Anonymity')
        if not isinstance(qi, list):
            raise TypeError("qi must be a list.")
        if not isinstance(sa, list):
            raise TypeError("sa must be a list.")

        # Assign values to instance variables
        self.qi = qi
        self.sa = sa
        self.alpha_threshold = alpha_threshold

    def check_dataset(self, df: DataFrame):
        alpha_k = anonymity.alpha_k_anonymity(df, self.qi, self.sa)[0]
        if not alpha_k:
            return {
                'message': '(Alpha, K)-anonymity check has failed.',
                'title': '(Alpha, K)-anonymity control',
                'status': False,
                'value': 0,
                'threshold': None
            }
        elif self.alpha_threshold < alpha_k:
            return {
                'message': '(Alpha, K)-anonymity check has failed. Either lower your alpha threshold or employ techniques to further anonymize this dataset if possible. (Alpha, K)-anonymity value: {alpha_k}',
                'title': '(Alpha, K)-anonymity control',
                'status': False,
                'value': alpha_k,
                'threshold': self.alpha_threshold
            }
        else:
            return {
                'message': '(Alpha, K)-anonymity check has passed.',
                'title': '(Alpha, K)-anonymity control',
                'status': True,
                'value': alpha_k,
                'threshold': self.alpha_threshold
            }