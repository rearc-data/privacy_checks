from runner import PrivacyRunner, CheckerSuites
import pandas as pd

# Make a fake dataframe with user, age and disease columns
df = pd.DataFrame(
    {
        "user": ["A", "B", "C", "D", "E", "F"],
        "age": [10, 10, 21, 23, 32, 35],
        "disease": ["flu", "asd", "cold", "sdaff", "nail", "sun"],
    }
)
# Create a PrivacyRunner object

custom_thresholds = {
    'k_threshold': 2,
    'alpha_threshold': 1,
    'l_threshold': 1,
    'entropy_l_threshold': 2,
    'c_threshold': 2,
    't_threshold': 1,
    'delta_threshold': 1
}
runner = PrivacyRunner(
    checkers=CheckerSuites.full_privacy_suite(qi=['user','age'], sa=['disease'], custom_thresholds=custom_thresholds),
    dry_run=True,
    full_suite_run=True)
runner.evaluate_data(df)
