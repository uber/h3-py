# Versioning

The H3 core library adheres to [Semantic Versioning](http://semver.org/).
H3-Py has a `major.minor.patch` version scheme. The major and minor version
numbers of H3-Py are the major and minor version of the bound core library,
respectively. The patch version is incremented independently of the core
library.

We use [this changelog structure](http://keepachangelog.com/).

Because H3-Py is versioned in lockstep with the H3 core library, please
avoid adding features or APIs which do not map onto the
[H3 core API](https://uber.github.io/h3/#/documentation/api-reference/).

## Unreleased

- None

## [3.7.7] - 2024-03-09

- Build Python 3.12 wheels (#344)

## [3.7.6] - 2022-11-23

- Build Python 3.11 wheels (#299)

## [3.7.5] - 2022-11-23

- BAD RELEASE

## [3.7.4] - 2022-04-14

- Website and API documentation; along with docstring cleanup.
- Add support for linters and IDE tooling (#213)
- Remove Py 3.5 wheel for Windows (#214)
- Py 3.10 wheels and on more architectures (#220, #221, #223, #225) 
- Greatly reduce sdist size (#227, #229)

## [3.7.3] - 2021-06-12

- Wheels for Linux Aarch64 (#189)

## [3.7.2] - 2021-03-01

- Add vectorized h3_to_parent and h3_get_resolution (#166)

## [3.7.1] - 2020-12-18

- fix for #169: `h3_distance` error reporting (#175)
- build Python 3.9 wheel for Mac (#175)
- bump h3lib version to v3.7.1 (#175)

## [3.7.0] - 2020-10-02

- Add functions (#171)
    + `cell_area`
    + `exact_edge_length`
    + `point_dist`

## [3.6.4] - 2020-07-20

- Add `requirements.in` for `pip-compile` usage (#157)
- Update `h3-c` to v3.6.4 (#157)
- Add functions:
    + `experimental_local_ij_to_h3` (#155)
    + `experimental_h3_to_local_ij` (#155)
    + `h3.unstable.vect.cell_haversine` (#147)
    + `h3.unstable.vect.geo_to_h3` (#147)
    + Prototype v4 names under `h3.unstable.v4` (#146)

## [3.6.3] - 2020-06-04

- Add functions:
    + `get_res0_indexes`
    + `h3_to_center_child`
    + `h3_get_faces`

## [3.6.2] - 2020-06-02

- Improve error reporting on `hex2int` (https://github.com/uber/h3-py/pull/127)
- Build Linux wheels for Python 2.7

## [3.6.1] - 2020-05-29

- Switch to Cython wrapper implementation
- Pre-built wheels on PyPI for Linux/Mac/Windows
- Provide multiple APIs:
    + `h3.api.basic_str`
    + `h3.api.basic_int`
    + `h3.api.numpy_int`
    + `h3.api.memview_int`

## [3.4.3] - 2019-04-18

- Removed null values in k_ring_distances.
- Support on Windows Platform
- Fixed some install problems

## [3.4.2] - 2019-03-13

- Added h3_line support.

## [3.1.0] - 2018-09-06

### Added
- Added h3_distance function.

### Changed
- Updated the core library to v3.1.0.

## [3.0.0] - 2018-07-24

### Added
- First public release.

