# Overview
This library is intended to demonstrate creating a wrapper library for common data scanning tools that are available for installation via pip.
As of now there are two included privacy check classes, Checker and MCProfiler. 
## Checker class
Checker is a wrapper for the [pycanon](https://pypi.org/project/pycanon/) library, that is described in detail in this [Nature article](https://www.nature.com/articles/s41597-022-01894-2).

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
An example instantiating the Checker class and setting all possible thresholds:

```python
from privacy_checks.checker import Checker
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
privacy_checker = Checker(
    qi=QI,
    df=user_df,
    sa=SA,
    k_threshold=5,
    alpha_threshold=0.5,
    beta_threshold=0.5,
    enhanced_beta_threshold=0.5,
    entropy_l_threshold=1,
    l_threshold=1,
    c_threshold=0.5,
    t_threshold=0.5
)
result = privacy_checker.run_tests_generate_report()
```
If you don't want to have any of the tests fail the notebook, you can simply not set the threshold for that test.  The test will still be run and results returned regardless.

## MCProfiler class
MCProfile is a wrapper for the DataProfiler library provided by Capital One, which is documented [here](https://github.com/capitalone/DataProfiler).

The MCProfiler class provides a few methods to generate a report, print metrics, perform a null roll check and detect PII columns.

You only need to pass this class a dataframe to utilize it.  An example of instantiating the class and running the methods is below:

```python
    from privacy_checks.mcprofiler import MCProfiler
    profile = MCProfiler(df=DATA)
    profile.generate_report()
    profile.null_row_check()
    profile.print_metrics()
    profile.detect_pii_columns()
```

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