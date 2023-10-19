from pandas import DataFrame
from pycanon import anonymity, report
from .basic_checker import BasicChecker

class DeltaDisclosurePrivacyChecker(BasicChecker):
    def __init__(
        self,
        qi: list,
        sa: list = [],
        delta_threshold: float = None,
    ):
        super().__init__('Delta-Disclosure Privacy')
        if not isinstance(qi, list):
            raise TypeError("qi must be a list.")
        if not isinstance(sa, list):
            raise TypeError("sa must be a list.")

        # Assign values to instance variables
        self.qi = qi
        self.sa = sa
        self.delta_threshold = delta_threshold

    def check_dataset(self, df: DataFrame):
        delta_disclosure_privacy = anonymity.delta_disclosure(df, self.qi, self.sa)
        if not delta_disclosure_privacy:
            return {
                'message': 'Delta-Disclosure Privacy check has failed.',
                'title': 'Delta-Disclosure Privacy control',
                'status': False,
                'value': 0,
                'threshold': None
            }
        elif self.delta_threshold < delta_disclosure_privacy:
            return {
                'message': 'Delta-Disclosure Privacy check has failed. Either lower your delta threshold or employ techniques to further anonymize this dataset if possible. Delta-Disclosure Privacy value: {delta_disclosure_privacy}',
                'title': 'Delta-Disclosure Privacy control',
                'status': False,
                'value': delta_disclosure_privacy,
                'threshold': self.delta_threshold
            }
        else:
            return {
                'message': 'Delta-Disclosure Privacy check has passed.',
                'title': 'Delta-Disclosure Privacy control',
                'status': True,
                'value': delta_disclosure_privacy,
                'threshold': self.delta_threshold
            }