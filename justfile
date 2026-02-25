export UV_NO_EDITABLE := "1"

_:
    just --list

reinstall:
    uv cache clean h3
    uv sync --extra test --reinstall-package h3

test: reinstall
    uv run pytest tests/test_lib --cov=h3 --cov=tests/test_lib --cov-fail-under=100

test-cython: reinstall
    uv run cythonize tests/test_cython/cython_example.pyx
    uv run pytest tests/test_cython --cov=tests/test_cython

lint:
    uv run ruff check

fix:
    uv run ruff check --fix

lab:
    uv sync --group docs
    uv run jupyter lab

build-docs:
    uv sync --group docs
    uv run jupyter-book build docs/ --warningiserror --keep-going --all

open:
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
    just _rm _skbuild
    just _rm .ruff_cache
    uv cache clean h3

_rm pattern:
    -@find . -name "{{pattern}}" -prune -exec rm -rf {} +
