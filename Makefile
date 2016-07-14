.PHONY: clean clean-pyc clean-test test

help:
	@echo "clean - remove all test and Python artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"

clean: clean-pyc clean-test

clean-pyc:
	find . -name "*.pyc" -exec rm -f {} \;
	find . -name "*.pyo" -exec rm -f {} \;
	find . -name "*~" -exec rm -f {} \;
	find . -name "__pycache__" -exec rm -fr {} \;

clean-test:
	rm -f tests/*.rst
	rm -f tests/*.html

test:
	py.test tests
