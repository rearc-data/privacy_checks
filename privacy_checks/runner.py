from pandas import DataFrame
from checkers.basic_checker import BasicChecker
from checkers.null_row_checker import NullRowChecker
from checkers.k_anonymity_checker import KAnonymityChecker
from checkers.alpha_k_anonymity_checker import AlphaKAnonymityChecker
from checkers.l_diversity_checker import LDiversityChecker
from checkers.entropy_l_diversity_checker import EntropyLDiversityChecker
from checkers.c_l_diversity_checker import CLDiversityChecker
from checkers.t_closeness_checker import TClosenessChecker
from checkers.delta_disclosure_privacy_checker import DeltaDisclosurePrivacyChecker


# Single entry point for interacting with utility instead of individual classes for each checker
# - Support providing df
# - Support defining a list of checkers 
# - Default checker lists / suites
class PrivacyRunner:
  def __init__(
        self,
        checkers: list[BasicChecker] = [],
        dry_run: bool = False,
        full_suite_run: bool = False,
        verbose: bool = True
    ):
    self.checkers = checkers
    self.dry_run = dry_run
    self.full_suite_run = full_suite_run
    self.verbose = verbose
    pass
  
  def build_response_str(self, checker_title, result):
    if result['status']:
      response_string = f"{checker_title} check passed."
      if result['value']:
        response_string += f" {checker_title} value: {result['value']}."
      if result['threshold']:
        response_string += f" {checker_title} threshold: {result['threshold']}."
    else:
      response_string = f"{checker_title} check failed."
      if result['value']:
        response_string += f" {checker_title} value: {result['value']}."
      if result['threshold']:
        response_string += f" {checker_title} threshold: {result['threshold']}."
    return response_string

  def evaluate_data(self, df: DataFrame):
    failed = False
    for checker in self.checkers:
      result = checker.check_dataset(df=df)
      #print(result)
      response_str = self.build_response_str(checker.title, result)
      if self.verbose:
        print(response_str)
      #test fails
      if not result['status']:
        failed = True;
        #if we don't want full suite to run, except here
        if not self.full_suite_run:
          raise Exception(response_str)
    if failed and not self.dry_run:
      raise Exception("Privacy checks failed.")

class CheckerSuites:
  def std_privacy_suite(qi: list, sa: list = [], custom_thresholds: dict = {}): 
    return [
      KAnonymityChecker(qi=qi, k_threshold=custom_thresholds.get('k_threshold', 5)),    
      NullRowChecker()
    ]
  def full_privacy_suite(qi: list, sa: list = [], custom_thresholds: dict = {}): 
    return [
      KAnonymityChecker(qi=qi, k_threshold=custom_thresholds.get('k_threshold', 5)),
      AlphaKAnonymityChecker(qi=qi, sa=sa, alpha_threshold=custom_thresholds.get('alpha_threshold', 0.5)),
      LDiversityChecker(qi=qi, sa=sa, l_threshold=custom_thresholds.get('l_threshold', 2)),
      EntropyLDiversityChecker(qi=qi, sa=sa, entropy_l_threshold=custom_thresholds.get('entropy_l_threshold', 2)),
      CLDiversityChecker(qi=qi, sa=sa, c_threshold=custom_thresholds.get('c_threshold', 2)),
      TClosenessChecker(qi=qi, sa=sa, t_threshold=custom_thresholds.get('t_threshold', 0.2)),
      DeltaDisclosurePrivacyChecker(qi=qi, sa=sa, delta_threshold=custom_thresholds.get('delta_threshold', 0.2)),
      NullRowChecker()
    ]
  
  # PrivacyRunner(checkers=CheckerSuite.std_privacy_suite(qi=['fake','columns'], sa=['disease'])).evaluate_data(df)