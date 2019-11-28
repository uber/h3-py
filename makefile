
DOCKER_IMAGE ?= quay.io/pypa/manylinux1_x86_64

.PHONY: purge init rebuild linux test lint lab

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

linux:
	docker run --rm -v `pwd`:/io ${DOCKER_IMAGE} /io/build-wheels-manylinux.sh

purge:
	rm -rf env MANIFEST .tox
	rm -rf .pytest_cache tests/__pycache__ __pycache__ _skbuild dist .coverage
	find . -type d -name '*.egg-info' | xargs rm -r
	find . -type f -name '*.pyc' | xargs rm -r
	find . -type d -name '*.ipynb_checkpoints' | xargs rm -r

test:
	env/bin/pytest tests/* --cov=h3 --cov-report term-missing

lint:
	flake8 src/h3 setup.py tests

lab:
	env/bin/pip install jupyterlab
	env/bin/jupyter lab
