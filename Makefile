test:
	python -m unittest discover tests

coverage:
	coverage run --source=wblib -m unittest discover tests
	coverage report
	coverage html

isort:
	isort --skip=venv

build:
	virtualenv -p python3.6 test_venv
	./test_venv/bin/pip install -r requirements.txt
	./test_venv/bin/python -m unittest discover tests
	rm -rf test_venv

venv:
	rm -rf venv
	virtualenv -p python3.6 venv
	./venv/bin/pip install -r requirements.txt

.PHONY: test coverage isort build venv
