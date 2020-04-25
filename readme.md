# README for Cython development branch

[![Build Status](https://travis-ci.com/uber/h3-py.svg?branch=cython)](https://travis-ci.com/uber/h3-py)
[![AppVeyor Status](https://ci.appveyor.com/api/projects/status/github/uber/h3-py?branch=cython&svg=true)](https://ci.appveyor.com/project/Uber/h3-py)
[![codecov](https://codecov.io/gh/uber/h3-py/branch/cython/graph/badge.svg)](https://codecov.io/gh/uber/h3-py)
[![version](https://img.shields.io/badge/h3-v3.6.1-blue.svg)](https://github.com/uber/h3/releases/tag/v3.6.1)
[![version](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

## Install for development

- `git clone git@github.com:uber/h3-py.git`
- `cd h3-py`
- `git checkout cython`
- `make init`
- `make test`
- `make lint`

Try from within `ipython`:

```
>>> import h3
>>> h3.geo_to_h3(0, 0, 0)
'8075fffffffffff'
```

## Install from GitHub

- `pip install scikit-build`
- `pip install git+https://github.com/uber/h3-py.git@cython`

## Docstrings

- Follow something like the [`numpydoc` docstring guide](https://numpydoc.readthedocs.io/en/latest/format.html)
  or the [`pandas` docstring guide](https://python-sprints.github.io/pandas/guide/pandas_docstring.html)


# Workflow

- [GitHub Standard Fork & Pull Request Workflow](https://gist.github.com/Chaser324/ce0505fbed06b947d962)
- [pyenv for multiple versions (to help with tox)](https://weknowinc.com/blog/running-multiple-python-versions-mac-osx)
- [tox stuff](https://blog.frank-mich.com/recipe-testing-multiple-python-versions-with-pyenv-and-tox/)
- [more tox stuff](https://blog.ionelmc.ro/2015/04/14/tox-tricks-and-patterns/)
