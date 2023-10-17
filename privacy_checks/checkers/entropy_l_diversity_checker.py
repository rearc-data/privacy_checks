from pandas import DataFrame
from pycanon import anonymity, report
from .basic_checker import BasicChecker

class EntropyLDiversityChecker(BasicChecker):
    def __init__(
        self,
        qi: list,
        sa: list = [],
        entropy_l_threshold: int = None,
    ):
        super().__init__('Entropy L-Diversity')
        if not isinstance(qi, list):
            raise TypeError("qi must be a list.")
        if not isinstance(sa, list):
            raise TypeError("sa must be a list.")

        # Assign values to instance variables
        self.qi = qi
        self.sa = sa
        self.entropy_l_threshold = entropy_l_threshold

    def check_dataset(self, df: DataFrame):
        entropy_l_div = anonymity.entropy_l_diversity(df, self.qi, self.sa)
        if not entropy_l_div:
            return {
                'message': 'Entropy L-diversity check has failed.',
                'title': 'Entropy L-diversity control',
                'status': False,
                'value': 0,
                'threshold': None
            }
        elif self.entropy_l_threshold < entropy_l_div:
            return {
                'message': 'Entropy L-diversity check has failed. Either lower your entropy L threshold or employ techniques to further anonymize this dataset if possible. Entropy L-diversity value: {entropy_l_div}',
                'title': 'Entropy L-diversity control',
                'status': False,
                'value': entropy_l_div,
                'threshold': self.entropy_l_threshold
            }
        else:
            return {
                'message': 'Entropy L-diversity check has passed.',
                'title': 'Entropy L-diversity control',
                'status': True,
                'value': entropy_l_div,
                'threshold': self.entropy_l_threshold
            }