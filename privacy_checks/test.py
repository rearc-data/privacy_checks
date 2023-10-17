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

runner = PrivacyRunner(checkers=CheckerSuites.full_privacy_suite(qi=['user','age'], sa=['disease']), dry_run=True, full_suite_run=True, verbose=True)
runner.evaluate_data(df)
