We separate the `h3-py` tests into two groups, organized by subfolder.

We do this because we expect 100% coverage on the library tests, but are
still working through getting full coverage on the Cython tests.


## `test_lib`

The tests in this folder are for the main `h3-py` Python API for folks
who are using the pure-Python library functionality.

## `test_cython`

The tests in this folder are for the advanced Cython API, that allows
for other *Cython* packages or scripts to use the Cython code provided
by the `h3-py` internals.

Note that the "Cython API" of `h3-py` is not currently externally supported.
