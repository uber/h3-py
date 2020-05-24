import os
from setuptools import find_packages
from skbuild import setup

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, 'src', 'h3', '_version.py')) as f:
    exec(f.read(), about)


def long_desc():
    here = os.path.abspath(os.path.dirname(__file__))
    fname = os.path.join(here, 'readme.md')
    with open(fname) as f:
        long_description = f.read()

    return long_description


setup(
    name = 'h3',
    version = about['__version__'],
    description = about['__description__'],
    long_description = long_desc(),
    long_description_content_type = 'text/markdown',
    license = about['__license__'],
    author = about['__author__'],
    author_email = about['__author_email__'],
    url = about['__url__'],
    classifiers = about['__classifiers__'],
    packages = find_packages(
        'src',
        exclude = ["*.tests", "*.tests.*", "tests.*", "tests"],
    ),
    package_dir = {'': 'src'},
    cmake_languages = ('C'),
    extras_require={
        'numpy': ['numpy'],
        'test': ['pytest', 'pytest-cov', 'flake8'],
        'all': ['numpy', 'pytest', 'pytest-cov', 'flake8'],
    },
)
