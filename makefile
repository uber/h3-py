.PHONY: init clear rebuild purge test lint lab ipython

PYTHON=$(shell command -v python || command -v python3)


build-docs:
	./env/bin/pip install -r requirements-dev.txt
	./env/bin/jupyter-book build docs/ --warningiserror --keep-going --all

open:
	open docs/_build/html/index.html

init: purge
	git submodule update --init
	$(PYTHON) -m venv env
	./env/bin/pip install --upgrade pip wheel setuptools
	./env/bin/pip install .[all]
	./env/bin/pip install -r requirements.in

clear:
	-./env/bin/pip uninstall -y h3
	-@rm -rf MANIFEST
	-@rm -rf annotations
	-@rm -rf .pytest_cache _skbuild dist .coverage build docs/_build
	-@find . -type d -name '__pycache__' | xargs rm -r
	-@find . -type d -name '*.egg-info' | xargs rm -r
	-@find . -type f -name '*.pyc' | xargs rm -r
	-@find . -type f -name '*.so' | xargs rm -r
	-@find . -type d -name '*.ipynb_checkpoints' | xargs rm -r
	-@find ./tests -type f -name '*.c' | xargs rm -r

rebuild: clear
	./env/bin/pip install .[all]

purge: clear
	-@rm -rf env

annotations: rebuild
	mkdir -p annotations
	cp _skbuild/*/cmake-build/src/h3/_cy/*.html ./annotations

test:
	./env/bin/cythonize -i tests/test_cython/cython_example.pyx
	./env/bin/pytest tests --cov=h3 --cov-report term-missing --durations=10

lint:
	./env/bin/flake8 src/h3 setup.py tests
	./env/bin/pylint --disable=all --enable=import-error tests/

lab:
	./env/bin/pip install -r requirements-dev.txt
	./env/bin/jupyter lab
