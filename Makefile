.PHONY: help install install-dev test lint format clean build docs pipeline

help:
	@echo "TravelPurpose - Makefile commands"
	@echo ""
	@echo "  make install       Install package"
	@echo "  make install-dev   Install package with dev dependencies"
	@echo "  make test          Run tests"
	@echo "  make lint          Run linters"
	@echo "  make format        Format code"
	@echo "  make clean         Clean build artifacts"
	@echo "  make build         Build package"
	@echo "  make pipeline      Run data pipeline (sample)"
	@echo "  make docs          Generate documentation"
	@echo ""

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	pytest --cov=travelpurpose --cov-report=term-missing --cov-report=html

test-fast:
	pytest -x -v

lint:
	ruff check travelpurpose/ tests/
	black --check travelpurpose/ tests/
	mypy travelpurpose/

format:
	black travelpurpose/ tests/ scripts/
	ruff check --fix travelpurpose/ tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -f .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

build: clean
	python -m build
	twine check dist/*

pipeline:
	python scripts/pipeline.py --sample 10 --verbose

pipeline-full:
	python scripts/pipeline.py --min-population 100000 --verbose

docs:
	@echo "Documentation is in README.md and examples/"
	@echo "Open examples/01_quickstart.ipynb for interactive examples"

.DEFAULT_GOAL := help
