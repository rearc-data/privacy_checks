from pandas import DataFrame
from .checkers.basic_checker import BasicChecker

# Single entry point for interacting with utility instead of individual classes for each checker
# - Support providing df
# - Support defining a list of checkers 
# - Default checker lists / suites
class PrivacyRunner:
  def __init__(
        self,
        checkers: list[BasicChecker] = [],
        dry_run: bool = False
    ):
    self.checkers = checkers
    pass

  def evaluate_data(self, df: DataFrame):
    failed_evaluations = []
    for checker in self.checkers:
      result = checker.check_dataset(df=df)
    

    # TODO: Report out failing checks, if at least one failed, throw exception if not dry_run

class CheckerSuites:
  def std_privacy_suite(cls, qi: list): 
    return []
  
  # PrivacyRunner(checkers=CheckerSuite.std_privacy_suite(...))