test:
	python -m unittest discover tests

coverage:
	coverage run --source=wattbikelib -m unittest discover tests
	coverage report
	coverage html

isort:
	isort --skip=venv
