# Makefile for Critter Counter development
# Makes common tasks easy to run

.PHONY: help setup test test-verbose test-coverage clean lint format run-sim simulate

help:
	@echo "Critter Counter - Available Commands"
	@echo "===================================="
	@echo "setup          - Create virtual environment and install dependencies"
	@echo "test           - Run all tests"
	@echo "test-verbose   - Run tests with verbose output"
	@echo "test-coverage  - Run tests with coverage report"
	@echo "lint           - Run code quality checks"
	@echo "format         - Auto-format code with black"
	@echo ""
	@echo "Simulation Commands:"
	@echo "simulate       - Run visual web simulation (recommended!)"
	@echo "simulate-cli   - Run command-line simulation"
	@echo "simulate-entry - Run CLI simulator with entry scenario"
	@echo "simulate-exit  - Run CLI simulator with exit scenario"
	@echo "simulate-multiple - Run CLI simulator with multiple cattle"
	@echo ""
	@echo "clean          - Remove generated files and caches"

setup:
	python3 -m venv venv
	@echo ""
	@echo "Virtual environment created!"
	@echo "Activate it with:"
	@echo "  source venv/bin/activate  (Mac/Linux)"
	@echo "  venv\\Scripts\\activate     (Windows)"
	@echo ""
	@echo "Then run: make install"

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	@echo "Dependencies installed!"

test:
	pytest

test-verbose:
	pytest -v

test-coverage:
	pytest --cov=src --cov-report=html --cov-report=term
	@echo ""
	@echo "Coverage report generated in htmlcov/index.html"

lint:
	pylint src/
	@echo "Linting complete!"

format:
	black src/ tests/
	@echo "Code formatted!"

type-check:
	mypy src/
	@echo "Type checking complete!"

simulate:
	@echo "Starting visual web simulation..."
	@echo "Open http://localhost:5000 in your browser"
	@python3 simulator/simulate_web.py

simulate-cli:
	python3 simulator/simulate.py

simulate-entry:
	python3 simulator/simulate.py --scenario entry

simulate-exit:
	python3 simulator/simulate.py --scenario exit

simulate-multiple:
	python3 simulator/simulate.py --scenario multiple


clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	@echo "Cleaned up generated files!"

# Quick test of specific module
test-counts:
	pytest tests/test_count_manager.py -v

test-direction:
	pytest tests/test_direction_detector.py -v

test-logger:
	pytest tests/test_data_logger.py -v

test-integration:
	pytest tests/test_integration.py -v
