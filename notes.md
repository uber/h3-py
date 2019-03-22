Based on @isaachier/h3-py
- https://github.com/isaachier/h3-py/blob/cython/src/h3core.pyx

- `git clone https://github.com/isaacbrodsky/h3-py.git`
- `cd h3-py`
- `git checkout aj`
- `git submodule update --init`
- `virtualenv -p python3 env`
- `source env/bin/activate`
- `pip install -r requirements-dev.txt`
- `python setup.py install`
- `pip install ipython; mkdir a; cd a; ipython`
- From within Pyhton: `import h3core.h3core`

- `source env/bin/activate`
- `python -m pytest ../test.py`

