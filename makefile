.PHONY: init clear rebuild purge test lint lab ipython


build-docs:
	env/bin/jupyter-book build docs/ --warningiserror --keep-going --all

open:
	open docs/_build/html/index.html


init: purge
	git submodule update --init
	python -m venv env
	env/bin/pip install --upgrade pip wheel setuptools
	env/bin/pip install .[all]
	env/bin/pip install -r requirements.in

clear:
	-env/bin/pip uninstall -y h3
	-@rm -rf MANIFEST
	-@rm -rf .pytest_cache tests/__pycache__ __pycache__ _skbuild dist .coverage
	-@find . -type d -name '*.egg-info' | xargs rm -r
	-@find . -type f -name '*.pyc' | xargs rm -r
	-@find . -type d -name '*.ipynb_checkpoints' | xargs rm -r

rebuild: clear
	env/bin/pip install .[all]

purge: clear
	-@rm -rf env

test:
	env/bin/pytest tests/* --cov=h3 --cov-report term-missing --durations=10

lint:
	env/bin/flake8 src/h3 setup.py tests
	env/bin/pylint --disable=all --enable=import-error tests/

lab:
	env/bin/pip install jupyterlab
	env/bin/jupyter lab
