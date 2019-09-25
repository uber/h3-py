# README for Cython development branch

Based on @isaachier/h3-py https://github.com/isaachier/h3-py/blob/cython/src/h3core.pyx

- `git clone git@github.com:ajfriend/h3-py.git`
- `cd h3-py`
- `git checkout <branch name>`
- `make init`
- `source env/bin/activate`

Try from within `ipython`:

```
>>> import h3
>>> h3.geo_to_h3(0, 0, 0)
'8075fffffffffff'
```

# to run tests
- `make test
