.PHONY: purge

purge:
	-@rm -rf env
	find src -type d -name '*.egg-info' | xargs rm -r
	find . -type f -name '*.pyc' | xargs rm -r
	find . -type d -name '*.ipynb_checkpoints' | xargs rm -r
	-@rm -rf .pytest_cache tests/__pycache__
