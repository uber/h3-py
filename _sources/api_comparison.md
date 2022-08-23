# API comparison

The `h3-py` library provides several APIs which share the same functions,
but differ in their input and output types:

- `h3.api.basic_str` (the *default* `import h3` is equivalent to `import h3.api.basic_str as h3`)
- `h3.api.basic_int`
- `h3.api.numpy_int`
- `h3.api.memview_int`

## Why are there multiple APIs?

<!-- TODO: if i make this a notebook, do i get to have the headings i want?
BETTER: keep as markdown, but let the launcher convert the markdown to a notebook for people to run and test! -->

Under the hood in the C library, H3 indices are represented as
unsigned 64-bit integers (`uint64_t`), and collections of indexes
are represented with C arrays.

For human readability, we often represent integer
indices (`578536630256664575`) in their
hexadecimal format (`8075fffffffffff`).

The *default* Python API (via `import h3` or `import h3.api.basic_str`),
represents indices in their hexadecimal
format as a Python `str`s and uses standard Python collection types like
`set` and `list`. These conventions make it more natural to work with
`h3-py` objects in Python, but come at the cost of converting back and forth
between the C and Python representations.

Alternative APIs like `h3.api.numpy_int` give up some of the Python conveniences to gain
speed by dealing with the C memory more directly and avoiding the conversion
costs.

Multiple APIs give users the power to choose the one that best fits their
needs, based on speed and convenience.

```{tip}
Note that the APIs are all 100% compatible, and it is easy to convert
between them with functions like `int_to_str` (links!) and `str_to_int`.

For example, one common pattern is to use `h3.api.numpy_int` for any
computationally-heavy work, and convert the output to `str` and `list`/`set`
(akin to `h3.api.basic_str`) to inspect or report the results.
```


## API Options

### `h3.api.basic_str`

H3 indexes are represented as Python `str`s,
using `list` and `set` for collections.

```python
>>> import h3
>>> h = h3.latlng_to_cell(0, 0, 0)
>>> h
'8075fffffffffff'

>>> h3.grid_ring(h, 1)
{'8055fffffffffff',
 '8059fffffffffff',
 '807dfffffffffff',
 '8083fffffffffff',
 '8099fffffffffff'}
```

````{note}
`basic_str` is the default API provided when you `import h3`. That is,

```python
import h3.api.basic_str as h3
```
and

```python
import h3
```

are equivalent.
````

### `h3.api.basic_int`

H3 indexes are represented as Python `int`s, using `list` and `set` for collections.

```python
>>> import h3.api.basic_int as h3
>>> h = h3.latlng_to_cell(0, 0, 0)
>>> h
578536630256664575

>>> h3.grid_ring(h, 1)
{577973680303243263,
 578044049047420927,
 578677367745019903,
 578782920861286399,
 579169948954263551}
```

### `h3.api.numpy_int`

H3 indexes are represented as `numpy.uint64`s, using `numpy.ndarray`
for collections.

The intention is for this API to be faster and more memory-efficient by
not requiring `int` to `str` conversion and by using
no-copy `numpy` arrays instead of Python `list`s and `set`s.

```python
>>> import h3.api.numpy_int as h3
>>> h = h3.latlng_to_cell(0, 0, 0)
>>> h
578536630256664575

>>> h3.grid_ring(h, 1)
array([578782920861286399, 578044049047420927, 577973680303243263,
       578677367745019903, 579169948954263551], dtype=uint64)
```

```{note}
`h3-py` has no runtime dependencies on other libraries, so the standard
`pip install h3` will not install any additional libraries.

However, `h3.api.numpy_int` does require `numpy`.
To install `numpy` (if it isn't already) along
with `h3`, you can run `pip install h3[numpy]`.
```

### `h3.api.memview_int`

H3 indexes are represented as `uint64`s, using Python
[`memoryview` objects](https://docs.python.org/dev/library/stdtypes.html#memoryview)
for collections.

This API has the same benefits as `numpy_int`, except it uses
(the less well-known but dependency-free) `memoryview`.
In fact, `h3.api.numpy_int` is essentially just a light wrapper around 
`h3.api.memview_int`.

```python
>>> import h3.api.memview_int as h3
>>> h = h3.latlng_to_cell(0, 0, 0)
>>> h
578536630256664575

>>> mv = h3.grid_ring(h, 1)
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

````{warning}
When using the `memview_int` API with the `numpy` library, note that the
[`numpy.array`](https://numpy.org/doc/stable/reference/generated/numpy.array.html)
conversion function **creates a copy** of the data.

On the other hand,
[`numpy.asarray`](https://numpy.org/doc/stable/reference/generated/numpy.asarray.html)
**does not create a copy**, and the
result points to the same memory location as the original `memoryview` object.

For example, consider the setup:

```python
>>> import h3.api.memview_int as h3
>>> import numpy as np
>>> h = h3.latlng_to_cell(0, 0, 0)
>>> mv = h3.grid_ring(h, 1)
>>> list(mv)
[578782920861286399,
 578044049047420927,
 577973680303243263,
 578677367745019903,
 579169948954263551]
```

Running `a = np.array(mv)` **creates a copy** of the memory view, so
modifying `mv` leaves `a` unchanged:

```python
>>> a = np.array(mv)
>>> mv[0] = 0
>>> a
array([578782920861286399, 578044049047420927, 577973680303243263,
       578677367745019903, 579169948954263551], dtype=uint64)
```

Running `a = np.asarray(mv)` **does not create a copy**, so modifying `mv` also
modifies `a`:

```python
>>> mv = h3.grid_ring(h, 1)
>>> a = np.asarray(mv)
>>> mv[0] = 0
>>> a
array([                 0, 578044049047420927, 577973680303243263,
       578677367745019903, 579169948954263551], dtype=uint64)
```
````


## API speed comparison

We time an example task to compare across APIs.

We also compare the option of doing most of the computation in one of the
faster APIs (using the `int` representation of H3 indexes),
and then converting the results to the more familiar
format of Python `str` objects.


### Example code

```python
import h3
import h3.api.numpy_int


def compute(h3_lib, N=100):
    h   = h3_lib.latlng_to_cell(0, 0, 9)
    out = h3_lib.grid_disk(h, N)
    out = h3_lib.compact_cells(out)
    
    return out

def compute_and_convert(h3_lib, N=100):
    out = compute(h3_lib, N)
    out = [h3.int_to_str(h) for h in out]
    
    return out
```

### Timing results

```{attention}
These are example timings on a single computer; you can run the
benchmarks yourself with the
[original notebook](https://github.com/uber/h3-py-notebooks/blob/master/notebooks/time_h3_apis.ipynb).
```


|         API          | `compute()` | `compute_and_convert()` |
|----------------------|-------------|-------------------------|
| `h3.api.basic_str`   | `59.8 ms`   | n/a                     |
| `h3.api.basic_int`   | `35.4 ms`   | `35.6 ms`               |
| `h3.api.memview_int` | `7.12 ms`   | `7.76 ms`               |
| `h3.api.numpy_int`   | `7.06 ms`   | `7.61 ms`               |


```{note}
For this example, we typically see about a 6--8x speedup between:

- computing with the `h3.api.basic_str` interface
- computing with the `h3.api.numpy_int` interface, and then converting the results back to `str`
```
