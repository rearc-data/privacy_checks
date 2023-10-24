from pandas import DataFrame
from pycanon import anonymity, report
from .basic_checker import BasicChecker


class KAnonymityChecker(BasicChecker):
    def __init__(
        self,
        # example_threshold: int = None,
    ):
        super().__init__('Insert Checker Name Here')

        # perform type checks here:
        # if not isinstance(example_threshold, int):
        #     raise TypeError("qi must be a list.")

        # Assign values to instance variables
        # self.example_threshold = example_threshold

    def check_dataset(self, df: DataFrame):
        # perform the logic needed to evaulate the dataset for the check

        value = 3 # replace this with the logic you want to use to check the dataset that evaulates to a score
        if value < self.example_threshold:
            return {
                'message': 'Add a descriptive message here that the end user will see if the check fails.',
                'title': 'Checker Name',
                'status': False,
                'value': value,
                'threshold': self.value
            }
        else:
            return {
                'message': 'Example check has passed.',
                'title': 'Checker Name',
                'status': True,
                'value': value,
                'threshold': self.example_threshold
            }

    
