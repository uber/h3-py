# README for Cython development branch

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
