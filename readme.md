<img align="right" src="https://uber.github.io/img/h3Logo-color.svg" alt="H3 Logo" width="200">

# h3-py

[![PyPI version](https://badge.fury.io/py/h3.svg)](https://badge.fury.io/py/h3)
[![version](https://img.shields.io/badge/h3-v3.6.3-blue.svg)](https://github.com/uber/h3/releases/tag/v3.6.1)
[![version](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

[![CI-linux](https://github.com/uber/h3-py/workflows/CI-linux/badge.svg)](https://github.com/uber/h3-py/actions)
[![CI-macos](https://github.com/uber/h3-py/workflows/CI-macos/badge.svg)](https://github.com/uber/h3-py/actions)
[![CI-windows](https://github.com/uber/h3-py/workflows/CI-windows/badge.svg)](https://github.com/uber/h3-py/actions)
[![codecov](https://codecov.io/gh/uber/h3-py/branch/master/graph/badge.svg)](https://codecov.io/gh/uber/h3-py)

Python bindings for the
[H3 Core Library](https://github.com/uber/h3).

For API reference, please see the
[H3 Documentation](https://h3geo.org/).

**NOTE: This version (v.3.6.1) corresponds to the new Cython
bindings, which have replaced the old bindings (v3.4.3).**


## Install from PyPI

`pip install h3`

Try the library with:

```python
>>> import h3
>>> lat, lng = 0, 0
>>> resolution = 0
>>> h3.geo_to_h3(lat, lng, resolution)
'8075fffffffffff'
```

## Example gallery

Browse [a collection of example notebooks](https://github.com/uber/h3-py-notebooks),
and if you have examples or visualizations of your own, please feel free to contribute!

We also have a simple [walkthrough of the API](https://nbviewer.jupyter.org/github/uber/h3-py-notebooks/blob/master/Usage.ipynb).
For more information, please see the [H3 Documentation](https://h3geo.org/).


## APIs

We provide multiple APIs in `h3-py`.

### `h3.api.basic_str`

H3 indexes are represented as Python `str`s, using `list` and `set` for collections.

This is the default API provided when you `import h3`.
That is, `import h3.api.basic_str as h3` and `import h3`
are basically equivalent.

```python
>>> import h3
>>> h = h3.geo_to_h3(0, 0, 0)
>>> h
'8075fffffffffff'

>>> h3.hex_ring(h, 1)
{'8055fffffffffff',
 '8059fffffffffff',
 '807dfffffffffff',
 '8083fffffffffff',
 '8099fffffffffff'}
```

### `h3.api.basic_int`

H3 indexes are represented as Python `int`s, using `list` and `set` for collections.

```python
>>> import h3.api.basic_int as h3
>>> h = h3.geo_to_h3(0, 0, 0)
>>> h
578536630256664575

>>> h3.hex_ring(h, 1)
{577973680303243263,
 578044049047420927,
 578677367745019903,
 578782920861286399,
 579169948954263551}
```

### `h3.api.numpy_int`

H3 indexes are represented as `unit64`s, using `numpy.ndarray`
for collections.

The intention is for this API to be faster and more memory-efficient by
not requiring `int` to `str` conversion and by using
no-copy `numpy` arrays instead of Python `list`s and `set`s.

```python
>>> import h3.api.numpy_int as h3
>>> h = h3.geo_to_h3(0, 0, 0)
>>> h
578536630256664575

>>> h3.hex_ring(h, 1)
array([578782920861286399, 578044049047420927, 577973680303243263,
       578677367745019903, 579169948954263551], dtype=uint64)
```

Note that `h3` has no runtime dependencies on other libraries, so a standard
`pip install` will install no additional libraries.
However, `h3.api.numpy_int` requires `numpy`. To have `numpy` installed (if it isn't already) along
with `h3`, run `pip install h3[numpy]`.


### `h3.api.memview_int`

H3 indexes are represented as `unit64`s, using Python
[`memoryview` objects](https://docs.python.org/dev/library/stdtypes.html#memoryview)
for collections.

This API has the same benefits as `numpy_int`, except it uses the
(less well-known) `memoryview` object.

```python
>>> import h3.api.memview_int as h3
>>> h = h3.geo_to_h3(0, 0, 0)
>>> h
578536630256664575

>>> mv = h3.hex_ring(h, 1)
>>> mv
<MemoryView of 'array' at 0x11188c710>

>>> mv[0]
578782920861286399

>>> list(mv)
[578782920861286399,
 578044049047420927,
 577973680303243263,
 578677367745019903,
 579169948954263551]
```

When using this API with `numpy`, note that `numpy.array` **creates a copy**
of the data, while `numpy.asarray` **does not create a copy** and the
result points to the same memory location as the `memoryview` object.

Continuing from the example above,

```python
>>> mv = h3.hex_ring(h, 1)
>>> a = np.array(mv)
>>> mv[0] = 0
>>> a
array([578782920861286399, 578044049047420927, 577973680303243263,
       578677367745019903, 579169948954263551], dtype=uint64)

>>> mv = h3.hex_ring(h, 1)
>>> a = np.asarray(mv)
>>> mv[0] = 0
>>> a
array([                 0, 578044049047420927, 577973680303243263,
       578677367745019903, 579169948954263551], dtype=uint64)
```
