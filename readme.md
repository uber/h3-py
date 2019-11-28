# README for Cython development branch

[![Build Status](https://travis-ci.com/uber/h3-py.svg?branch=cython)](https://travis-ci.com/uber/h3-py)
[![AppVeyor Status](https://ci.appveyor.com/api/projects/status/github/uber/h3-py?branch=cython&svg=true)](https://ci.appveyor.com/project/Uber/h3-py)
[![codecov](https://codecov.io/gh/uber/h3-py/branch/cython/graph/badge.svg)](https://codecov.io/gh/uber/h3-py)

Based on https://github.com/uber/h3-py/tree/cython

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


# Workflow

- [GitHub Standard Fork & Pull Request Workflow](https://gist.github.com/Chaser324/ce0505fbed06b947d962)
