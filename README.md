# Overview
This library is intended to demonstrate creating a wrapper library for common data scanning tools that are available for installation via pip.
As of now there are 12 included privacy checks that can be run against a dataset. 
## Checker class
A number of them are wrappers for the [pycanon](https://pypi.org/project/pycanon/) library, that is described in detail in this [Nature article](https://www.nature.com/articles/s41597-022-01894-2).
The rest are wrappers for the DataProfiler library provided by Capital One, which is documented [here](https://github.com/capitalone/DataProfiler).

At a minimum, you need to provide the class a set of [Quasi identifiers](https://en.wikipedia.org/wiki/Quasi-identifier) in order to perform a k-anonymity, which is represented by a list of of the column names from the dataframe written as strings.
In order to take advantage of other metrics available such as l-diversity, you will also need to provide a single (or set) of [Sensitive Attributes](https://arx.deidentifier.org/overview/privacy-criteria/), which is described as
"Sensitive attributes encode properties with which individuals are not willing to be linked with. As such, they might be of interest to an attacker and, if disclosed, could cause harm to data subjects. They will be kept unmodified but may be subject to further constraints, such as t-closeness or l-diversity. Typical examples are diagnoses."

If you provide both a list of QI's and SA's, the entire test suite will be run and a report generated.  The tests available are the following:
- [K-Anonymity](https://pycanon.readthedocs.io/en/latest/pycanon.anonymity.html#pycanon.anonymity.k_anonymity)
- [Alpha K-Anonymity](https://pycanon.readthedocs.io/en/latest/pycanon.anonymity.html#pycanon.anonymity.alpha_k_anonymity)
- [Basic Beta Likeness](https://pycanon.readthedocs.io/en/latest/pycanon.anonymity.html#pycanon.anonymity.basic_beta_likeness)
- [Delta Disclouse](https://pycanon.readthedocs.io/en/latest/pycanon.anonymity.html#pycanon.anonymity.delta_disclosure)
- [Enhance Beta Likeness](https://pycanon.readthedocs.io/en/latest/pycanon.anonymity.html#pycanon.anonymity.enhanced_beta_likeness)
- [Entropy L-Diversity](https://pycanon.readthedocs.io/en/latest/pycanon.anonymity.html#pycanon.anonymity.entropy_l_diversity)
- [L-Diversity](https://pycanon.readthedocs.io/en/latest/pycanon.anonymity.html#pycanon.anonymity.l_diversity)
- [Recursive (c,l)-diversity](https://pycanon.readthedocs.io/en/latest/pycanon.anonymity.html#pycanon.anonymity.recursive_c_l_diversity)
- [T-Closeness](https://pycanon.readthedocs.io/en/latest/pycanon.anonymity.html#pycanon.anonymity.t_closeness)

If you want to block execution of a notebook based on the results of any of these tests, you can provide thresholds for each when instantiating the class that will be checked against the actual value, and if the threshold is breached, the test suite will fail and throw an exception.
- K-Anonymity = k_threshold (int)
- Alpha K-Anonymity = alpha_threshold (float)
- Basic Beta Likeness = beta_threshold (float)
- Enhance Beta Likeness = enhanced_beta_threshold (float)
- Entropy L-Diversity = entropy_l_threshold (int)
- L-Diversity = l_threshold (int)
- Recursive (c,l)-diversity = c_threshold (float)
- T-Closeness = t_threshold (float)

An example instantiating the Runner class and setting all possible thresholds:

```python
from privacy_checks.runner import PrivacyRunner, CheckerSuites
# replace with your dataset you want to target
users_df = spark.read.table('unicorn_app.synthetic.users_indexed')
users_df = users_df.toPandas()
# add the quasi identifiers (columns) you want to check
QI = [
    'Gender',
    'City',
    'State',
]
# add any columns that would be consider sensitive attributes
SA = ["FICO_Score"]
custom_thresholds = {
    'k_threshold': 2,
    'alpha_threshold': 1,
    'l_threshold': 1,
    'entropy_l_threshold': 2,
    'c_threshold': 2,
    't_threshold': 1,
    'delta_threshold': 1
}

runner = PrivacyRunner(checkers=CheckerSuites.full_privacy_suite(qi=qi, sa=sa, custom_thresholds=custom_thresholds), dry_run=False, full_suite_run=True, verbose=True)
runner.evaluate_data(users_df)
```
If you don't want to have any of the tests fail the notebook, you can set dry_run to True.  The test will still be run and results returned regardless, but it will not fail the rest of the notebook execution.

To just run the standard set of tests, which is K-Anonymity, PII Detection and a null row check you would do:
```python
from privacy_checks.runner import PrivacyRunner, CheckerSuites
qi = ['Gender', 'City','State']
sa = ['FICO_Score']
runner = PrivacyRunner(checkers=CheckerSuites.std_privacy_suite(qi=qi, sa=sa), dry_run=False, full_suite_run=True, verbose=True)
runner.evaluate_data(df)
```

# Extending the Library
The library was built based on the idea that new "checkers" could be easily added by engineers as business needs arise. The file basic_checker.py is what needs to be extended in order to create a new checker.

Each new checker should overload the base function "check_dataset" with the logic you want to execute when the test suite is run.
Make sure to make the return dict as pictured here:
```
    # {
    #   message: str,
    #   title: str <k-anonmity control>,
    #   status: bool,
    #   value: float OPTIONAL,
    #   threshold: float OPTIONAL
    # }
```
Please note for all checks the concept of a value being returned (beyond just a pass/fail status), or a threshold being set may not exist.  For this reason these are optional return keys, and if a checker does not return them, the library will elegantly handle this when creating a report.

If you add a new check, or you want to define a custom set of "checkers" to be run for a certain test suite, you can edit the class CheckerSuites, located in runner.py.

Imagine we wanted to add the PII Check to the standard privacy suite - we could edit the class as such:
```
from privacy_checks.checkers.basic_checker import BasicChecker
from privacy_checks.checkers.null_row_checker import NullRowChecker
from privacy_checks.checkers.pii_checker import PIIChecker
...
class CheckerSuites:
  def std_privacy_suite(qi: list, sa: list = [], custom_thresholds: dict = {}): 
    return [
      KAnonymityChecker(qi=qi, k_threshold=custom_thresholds.get('k_threshold', 5)),    
      NullRowChecker()
    ]
```
Would become:
```
class CheckerSuites:
  def std_privacy_suite(qi: list, sa: list = [], custom_thresholds: dict = {}): 
    return [
      KAnonymityChecker(qi=qi, k_threshold=custom_thresholds.get('k_threshold', 5)),    
      NullRowChecker(),
      PIIChecker()
    ]
```

In here we can also declare a number of different test suite combinations, and set custom thresholds for each. You can imagine a scenario where we make suites that utilize the same tests, but have different more restrictive thresholds set - and how this could be utilized to "grade" the state of datasets.

# Packaging the library
This python library uses [setuptools](https://setuptools.pypa.io/en/latest/userguide/quickstart.html#) to manage the packaging of the library.

The project dependencies and details are described in [pyproject.toml](pyproject.toml).

If needed, install the build tool:
```shell
pip install --upgrade build
```

Then build this project:
```
python -m build
```

Which will generate a `tar.gz` and `.whl` file in the `dist` directory.

You can just upload the wheel file and install from there, this will be more efficient than installing from the source distribution.

# Install

You can use pip to install this library on Databricks.  Upload the packaged wheel file to a volume in the databricks workspace you want to utilize it from and then target it with a pip install command:
```notebook
%pip install privacy_checks -f /Volumes/path/to/package
```