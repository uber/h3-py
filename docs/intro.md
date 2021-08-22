# **h3-py**: Uber's H3 Hexagonal Hierarchical Geospatial Indexing System in Python

TODO: have this guy read from the README, just like we do with the changelog
Nice and DRY!

Python bindings for the
[H3 Core Library](https://github.com/uber/h3).

## Installation

From [PyPI](https://pypi.org/project/h3/):

```
pip install h3
```

From [conda](https://github.com/conda-forge/h3-py-feedstock):

```sh
conda config --add channels conda-forge
conda install h3-py
```

## Usage

```python
>>> import h3
>>> lat, lng = 37.769377, -122.388903
>>> resolution = 9
>>> h3.geo_to_h3(lat, lng, resolution)
'89283082e73ffff'
```

## Example gallery

Browse [a collection of example notebooks](https://github.com/uber/h3-py-notebooks),
and if you have examples or visualizations of your own, please feel free to contribute!

We also have a simple [walkthrough of the API](https://nbviewer.jupyter.org/github/uber/h3-py-notebooks/blob/master/notebooks/usage.ipynb).
For more information, please see the [H3 Documentation](https://h3geo.org/).
