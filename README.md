# Install

You can use pip to install this library on Databricks.  Upload it to a volume in the databricks workspace you want to utilize it from, then target it with a pip install command:

    %pip install privacy_checks -f /Volumes/path/to/package

# Utilization

To utilize the included packages, you can use the following examples:

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
    DATA = users_df
    privacy_checker = Checker(qi=QI, df=DATA.head(20), sa=SA)
    result = privacy_checker.run_tests_generate_report()

    from privacy_checks.mcprofiler import MCProfiler
    profile = MCProfiler(df=DATA)
    profile.generate_report()
    profile.null_row_check()
    profile.print_metrics()
    profile.detect_pii_columns()
# To Build The Package for Install - 
    python setup.py sdist bdist_wheel