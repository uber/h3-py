# README for Cython development branch

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

# trying to pip install from the repo

- try `env/bin/pip install git+https://github.com/uber/h3-py.git@cython`
- but we get a cython error


