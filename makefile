
DOCKER_IMAGE ?= quay.io/pypa/manylinux1_x86_64

.PHONY: purge init rebuild linux test

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
	-@rm -rf env
	find src -type d -name '*.egg-info' | xargs rm -r
	find . -type f -name '*.pyc' | xargs rm -r
	find . -type d -name '*.ipynb_checkpoints' | xargs rm -r
	-@rm -rf .pytest_cache tests/__pycache__ __pycache__ _skbuild dist

test:
	env/bin/pytest tests/test.py
