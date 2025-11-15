PYTHON = python


# Formatters
format: black

black:
	$(PYTHON) -m black onotation/ tests/


# Linters
lint: ruff mypy

mypy:
	$(PYTHON) -m mypy onotation/ tests/

ruff:
	$(PYTHON) -m ruff check onotation/ tests/


# Tests
test: unit-tests

unit-tests:
	$(PYTHON) -m pytest tests/
