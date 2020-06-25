from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path
import parserGenerator

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ParserGen',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # http://packaging.python.org/en/latest/tutorial.html#version
    version=nn_benchmark.__version__,

    description='Parser Generator from an input EBNF grammar',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/QDucasse/ParserGen',

    # Author details
    author='Quentin Ducasse, Kevin Bedin',
    author_email='quentin.ducasse@ensta-bretagne.org, kevin.bedin@ensta-bretagne.org',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Topic :: Utilities',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.8',

        'Operating System :: Apple :: macOS',
    ],

    # What does your project relate to?
    keywords='EBNF parser lexer ast visitor grammar',

    packages=find_packages(),

    install_requires=['Jinja2'],

)
