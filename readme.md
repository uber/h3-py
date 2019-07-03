# README for Cython development branch

Based on @isaachier/h3-py https://github.com/isaachier/h3-py/blob/cython/src/h3core.pyx

- `git clone git@github.com:ajfriend/h3-py.git`
- `cd h3-py`
- `git checkout <branch name>`
- `make init`
- `source env/bin/activate`

Try from within `ipython`:

Note: Can't be in top-level directory, since there is a folder named `h3py` and python will try to import from that, which is not what we want. We only
want to run the installed version. Just change to a different directory, like `tests`.

```
>>> import h3py.h3core as h3
>>> h3.geo_to_h3(0, 0, 0)
'8075fffffffffff'
```

# to run tests
- `make test`
