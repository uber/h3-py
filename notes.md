- https://github.com/isaachier/h3-py/blob/cython/src/h3core.pyx

- `git clone https://github.com/isaachier/h3-py.git`
- `cd h3-py`
- `git submodule update --init`
- `git checkout cython`
- `virtualenv -p python3 env`
- `source env/bin/activate`
- `pip install -r requirements-dev.txt`
- `pip install cython`
- `mkdir build; cd build; cmake -DCMAKE_BUILD_TYPE=Debug ..`
- from within build dir: `make`


- `fab bootstrap` (maybe not needed?)

