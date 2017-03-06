test:
	python -m unittest discover tests

coverage:
	coverage run --source=wblib -m unittest discover tests
	coverage report
	coverage html

isort:
	isort --skip=venv
