# API Types

We provide multiple APIs in `h3-py`.
All APIs have the same set of functions, but differ
in their input/output formats.

## `h3.api.basic_str`

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

## `h3.api.basic_int`

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

## `h3.api.numpy_int`

H3 indexes are represented as `uint64`s, using `numpy.ndarray`
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


## `h3.api.memview_int`

H3 indexes are represented as `uint64`s, using Python
[`memoryview` objects](https://docs.python.org/dev/library/stdtypes.html#memoryview)
for collections.

This API has the same benefits as `numpy_int`, except it uses
(the less well-known but dependency-free) `memoryview`.

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
