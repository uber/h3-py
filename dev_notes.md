# Development notes for `h3-py`

## Install for development

This repo uses [`just`](https://github.com/casey/just) for running common development commands.

To get started:

- `git clone git@github.com:uber/h3-py.git`
- `cd h3-py`
- `just lint`
- `just test`
- `just test-cython`

To build and view docs:

- `just docs`
- `just view`


## Docstrings

- Follow something like the [`numpydoc` docstring guide](https://numpydoc.readthedocs.io/en/latest/format.html)
  or the [`pandas` docstring guide](https://python-sprints.github.io/pandas/guide/pandas_docstring.html)

## Updating the H3 submodule

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

## Resetting the submodule

For when moving between `h3-py` branches using different versions of the
`h3lib` submodule.

```sh
git submodule deinit -f .
git submodule update --init
```

## Releasing a new version

- update `CHANGELOG.md` to reflect any changes since the last release
- update the `h3-py` version in `pyproject.toml`
- if updating the C `h3lib` version, update the version badge on the readme
- create PR, get reviews, and merge with these changes
- go to https://github.com/uber/h3-py/releases and "Draft a new release"
    - set the tag version and the release to the version. e.g., `v3.7.2`
      (alternatively: `git tag v3.7.2` && `git push origin --tags`)
    - add the updated `CHANGELOG.md` text to the release notes
    - publish release
- GitHub actions should trigger on the release event and then go on to build
  and upload the wheels to PyPI
