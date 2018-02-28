# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
long_description = "see https://github.com/JoinVerse/vid for more info."

setup(
    name='vid',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='1.0.0',

    description='Python Vid Implementation',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/JoinVerse/vid',

    # Author details
    author='JoinVerse',
    author_email='',

    # Choose your license
    license='MIT',

    py_modules=['vid', 'base32hex'],
    download_url='',
)
