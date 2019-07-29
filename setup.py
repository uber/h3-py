import os
from setuptools import find_packages
from skbuild import setup


here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, 'h3py', '__version__.py')) as f:
    exec(f.read(), about)

setup(
    name='h3py',
    version=about['__version__'],
    description=
    'Python bindings for H3, a hierarchical hexagonal geospatial indexing system developed by Uber Technologies',
    long_description='long_description',
    author='Uber Technologies',
    author_email='Niel Hu <hu.niel92@gmail.com>',
    url='https://github.com/uber/h3-py.git',
    packages=find_packages(),
    classifiers=[
        "Development Status :: 2 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: C",
        "Programming Language :: Cython",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    cmake_languages=('C'),
)
