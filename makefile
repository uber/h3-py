.PHONY: purge init rebuild test lint lab tox

init: purge
	git submodule update --init
	virtualenv -p python3 env
	env/bin/pip install -r requirements-dev.txt
	env/bin/python setup.py bdist_wheel
	env/bin/pip install dist/*.whl

rebuild:
	env/bin/python setup.py bdist_wheel
	env/bin/pip uninstall -y h3
	env/bin/pip install dist/*.whl

purge:
	rm -rf env MANIFEST .tox
	rm -rf .pytest_cache tests/__pycache__ __pycache__ _skbuild dist .coverage
	find . -type d -name '*.egg-info' | xargs rm -r
	find . -type f -name '*.pyc' | xargs rm -r
	find . -type d -name '*.ipynb_checkpoints' | xargs rm -r

test:
	env/bin/pytest tests/* --cov=h3 --cov-report term-missing --durations=10

tox:
	tox

lint:
	flake8 src/h3 setup.py tests

lab:
	env/bin/pip install jupyterlab
	env/bin/jupyter lab

ipython:
	env/bin/pip install ipython
	env/bin/ipython
