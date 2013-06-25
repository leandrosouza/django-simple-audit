# Makefile for simple_audit

help:
	@echo
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  clean      to clean garbage left by builds and installation"
	@echo "  compile    to compile .py files (just to check for syntax errors)"
	@echo "  install    to install"
	@echo "  build      to build without installing"
	@echo "  dist       to create egg for distribution"
	@echo "  publish    to publish the package to PyPI"
	@echo

clean:
	@echo "Cleaning..."
	@rm -rf build dist *.egg-info *.pyc **/*.pyc *~

compile: clean
	@echo "Compiling source code..."
	@python -tt -m compileall simple_audit
	@python -tt -m compileall tests

install:
	@python setup.py install

build:
	@python setup.py build

dist: clean
	@python setup.py sdist

publish: clean
	@python setup.py sdist upload -r epypi
