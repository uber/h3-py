<img align="right" src="https://uber.github.io/img/h3Logo-color.svg" alt="H3 Logo" width="200">

# h3-py

[![PyPI version](https://badge.fury.io/py/h3.svg)](https://badge.fury.io/py/h3)
[![version](https://img.shields.io/badge/h3-v3.6.1-blue.svg)](https://github.com/uber/h3/releases/tag/v3.6.1)
[![version](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

![](https://github.com/uber/h3-py/workflows/CI-linux/badge.svg)
[![Build Status](https://travis-ci.com/uber/h3-py.svg?branch=cython)](https://travis-ci.com/uber/h3-py)
[![AppVeyor Status](https://ci.appveyor.com/api/projects/status/github/uber/h3-py?branch=cython&svg=true)](https://ci.appveyor.com/project/Uber/h3-py)
[![codecov](https://codecov.io/gh/uber/h3-py/branch/master/graph/badge.svg)](https://codecov.io/gh/uber/h3-py)

Python bindings for the
[H3 Core Library](https://github.com/uber/h3).

For API reference, please see the
[H3 Documentation](https://h3geo.org/).

**NOTE: This version (v.3.6.1) corresponds to the new Cython
bindings, which will replace the old bindings (v3.4.3).
This version is not yet published to PyPI.**

## Install from PyPI

TODO: instructions for installing from pre-built wheels

## Install from GitHub

You need to have `cc`, `make`, `cmake`, and `git` in your `$PATH` when installing this package.

Then run:
- `pip install git+https://github.com/uber/h3-py.git`

Try the library with:

```python
>>> import h3
>>> h3.geo_to_h3(0, 0, 0)
'8075fffffffffff'
```

## Example gallery

Browse [a collection of example notebooks](https://github.com/uber/h3-py-notebooks),
and if you have examples or visualizations of your own, please feel free to contribute!

We also have a simple [walkthrough of the API](https://nbviewer.jupyter.org/github/uber/h3-py-notebooks/blob/master/Usage.ipynb).
For more information, please see the [H3 Documentation](https://h3geo.org/).
