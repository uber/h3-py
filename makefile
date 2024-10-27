.PHONY: init clear rebuild purge test lint lab ipython

PYTHON=$(shell command -v python || command -v python3)


build-docs:
	./env/bin/pip install .[all]
	./env/bin/jupyter-book build docs/ --warningiserror --keep-going --all

open:
	open docs/_build/html/index.html

init: purge
	git submodule update --init
	$(PYTHON) -m venv env
	./env/bin/pip install --upgrade pip wheel setuptools
	./env/bin/pip install .[test]

clear:
	-./env/bin/pip uninstall -y h3
	-@rm -rf MANIFEST
	-@rm -rf .pytest_cache _skbuild dist .coverage build docs/_build .ruff_cache
	-@find . -type d -name '__pycache__' | xargs rm -r
	-@find . -type d -name '*.egg-info' | xargs rm -r
	-@find . -type f -name '*.pyc' | xargs rm -r
	-@find . -type f -name '*.so' | xargs rm -r
	-@find . -type d -name '*.ipynb_checkpoints' | xargs rm -r
	-@find ./tests -type f -name '*.c' | xargs rm -r
	-@find ./tests -type f -name '*.html' | xargs rm -r

rebuild: clear
	./env/bin/pip install .[test]

purge: clear
	-@rm -rf env

test:
	./env/bin/pip install cython
	./env/bin/cythonize tests/test_cython/cython_example.pyx
	./env/bin/pytest

lint:
	./env/bin/ruff check

fix:
	./env/bin/ruff check --fix

lab:
	./env/bin/pip install .[all]
	./env/bin/jupyter lab
