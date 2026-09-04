.PHONY: install test lint typecheck smoke package

install:
	python -m pip install -e '.[dev]'

test:
	pytest -q

lint:
	ruff check src tests

typecheck:
	mypy src

smoke:
	python -m bclosure.cli inspect configs/synthetic_hadamard.yaml
	python -m bclosure.cli benchmark configs/synthetic_hadamard.yaml

package:
	python scripts/build_manifest.py
