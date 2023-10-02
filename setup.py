from setuptools import setup, find_packages

setup(
    name="privacy_checks",  # Replace with your desired package name
    version="0.1",
    author="Mark deGroat",
    author_email="mark.degroat@rearc.io",
    description="A Python library for privacy checks",
    long_description="A Python library for performing various privacy checks on data.",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "pandas",  # Add any dependencies your library uses
        "pycanon",  # Add any other dependencies here
        "dataprofiler[ml]",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)