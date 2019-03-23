.PHONY: purge init

init:
	git submodule update --init
	virtualenv -p python3 env
	env/bin/pip install -r requirements-dev.txt
	env/bin/python setup.py install

purge:
	-@rm -rf env
	find src -type d -name '*.egg-info' | xargs rm -r
	find . -type f -name '*.pyc' | xargs rm -r
	find . -type d -name '*.ipynb_checkpoints' | xargs rm -r
	-@rm -rf .pytest_cache tests/__pycache__ __pycache__ _skbuild dist h3.egg-info
