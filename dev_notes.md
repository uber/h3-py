# Development notes for `h3-py`

## Install for development

- `git clone git@github.com:uber/h3-py.git`
- `cd h3-py`
- `make init`
- `make test`
- `make lint`


## Docstrings

- Follow something like the [`numpydoc` docstring guide](https://numpydoc.readthedocs.io/en/latest/format.html)
  or the [`pandas` docstring guide](https://python-sprints.github.io/pandas/guide/pandas_docstring.html)


# Workflow

- [GitHub Standard Fork & Pull Request Workflow](https://gist.github.com/Chaser324/ce0505fbed06b947d962)
- [pyenv for multiple versions (to help with tox)](https://weknowinc.com/blog/running-multiple-python-versions-mac-osx)
- [tox stuff](https://blog.frank-mich.com/recipe-testing-multiple-python-versions-with-pyenv-and-tox/)
- [more tox stuff](https://blog.ionelmc.ro/2015/04/14/tox-tricks-and-patterns/)


# Updating the H3 submodule

```sh
cd src/h3lib
git checkout master
git pull
cd ..
git add h3lib
git commit ...
```

for a specific version tag:

```sh
cd src/h3lib
git checkout v3.7.1  # or whatever version tag you'd like
cd ..
git add h3lib
git commit ...
```
