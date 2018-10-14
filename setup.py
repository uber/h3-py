import os
import sys
import platform
import subprocess
from setuptools import find_packages
from skbuild import setup

from version import version

long_description = open('README.rst').read()

setup(
    name='h3',
    version=version,
    description=
    'Python bindings for H3, a hierarchical hexagonal geospatial indexing system developed by Uber Technologies',
    long_description=long_description,
    author='Uber Technologies',
    author_email='Niel Hu <hu.niel92@gmail.com>',
    url='https://github.com/uber/h3-py.git',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[],
)
