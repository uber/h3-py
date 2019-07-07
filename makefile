DOCKER_IMAGE ?= quay.io/pypa/manylinux1_x86_64

.PHONY: purge init


init: purge
	git submodule update --init
	virtualenv -p python3 env
	env/bin/pip install -r requirements-dev.txt
	env/bin/python setup.py bdist_wheel
	env/bin/pip install dist/*.whl


rebuild:
	env/bin/python setup.py bdist_wheel
	env/bin/pip uninstall -y h3py
	env/bin/pip install dist/*.whl
	env/bin/python -Ic 'from h3py import h3core; print(h3core.__file__)'
	env/bin/python -Ic 'from h3py import hexmem; print(hexmem.__file__)'


linux:
	docker run --rm -v `pwd`:/io ${DOCKER_IMAGE} /io/build-wheels-manylinux.sh


purge:
	-@rm -rf env
	find . -type d -name '*.egg-info' | xargs rm -r
	find . -type f -name '*.pyc' | xargs rm -r
	find . -type d -name '*.ipynb_checkpoints' | xargs rm -r
	-@rm -rf .pytest_cache tests/__pycache__ __pycache__ _skbuild dist h3.egg-info


test:
	env/bin/pytest tests/test.py
