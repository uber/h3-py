# disable editable installs so uv sync does a full build of the C extension
export UV_NO_EDITABLE := "1"

_:
    just --list

# force-rebuild the C extension to avoid stale builds
reinstall:
    uv cache clean h3
    uv sync --reinstall-package h3

# locally, always reinstall before testing
test: reinstall ci-test
test-cython: reinstall ci-test-cython

fix:
    uvx ruff check --fix

lab:
    uv sync --group docs
    uv run jupyter lab

view:
    open docs/_build/html/index.html

purge:
    just _rm .venv
    just _rm '*.pytest_cache'
    just _rm .DS_Store
    just _rm '*.egg-info'
    just _rm dist
    just _rm '*.ipynb_checkpoints'
    just _rm __pycache__
    just _rm uv.lock
    just _rm .coverage
    just _rm build
    just _rm _build
    just _rm _skbuild
    just _rm .ruff_cache
    uv cache clean h3

_rm pattern:
    -@find . -name "{{pattern}}" -prune -exec rm -rf {} +


# Recipes below are used by CI workflows (.github/workflows/).
# Changes here may break CI — update the workflows accordingly.

ci-test:
    uv run pytest tests/test_lib --cov=h3 --cov=tests/test_lib --cov-fail-under=100

ci-test-cython:
    uv run --with cython --with setuptools cythonize tests/test_cython/cython_example.pyx
    uv run pytest tests/test_cython --cov=tests/test_cython

lint:
    uvx ruff check

docs:
    uv sync --group docs
    uv run jupyter-book build docs/ --warningiserror --keep-going --all
