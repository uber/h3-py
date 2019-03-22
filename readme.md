# README for Cython development branch

Based on @isaachier/h3-py https://github.com/isaachier/h3-py/blob/cython/src/h3core.pyx

- `git clone https://github.com/isaacbrodsky/h3-py.git`
- `cd h3-py`
- `git checkout cython`
- `git submodule update --init`
- `virtualenv -p python3 env`
- `source env/bin/activate`
- `pip install -r requirements-dev.txt`
- `python setup.py install`
- `cd tests; ipython`
- From within IPython: `import h3core.h3core as h3`
- `h3.geo_to_h3(0, 0, 0)`

# to run tests
- `source env/bin/activate`
- `cd tests`
- `pytest test.py`
