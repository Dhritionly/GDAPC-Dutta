# Makefile for GDAPC-Dutta Data Analysis Project
# Provides convenient commands for development, testing, and deployment

.PHONY: help install test lint format clean run-examples setup-dev check-all

# Default target
help:
	@echo "GDAPC-Dutta Data Analysis Project - Available Commands:"
	@echo ""
	@echo "  install        Install project dependencies"
	@echo "  setup-dev      Set up development environment"
	@echo "  test           Run all tests"
	@echo "  test-verbose   Run tests with verbose output"
	@echo "  test-coverage  Run tests with coverage report"
	@echo "  lint           Run code linting (flake8)"
	@echo "  format         Format code with black"
	@echo "  type-check     Run type checking with mypy"
	@echo "  check-all      Run all quality checks (lint, format-check, type-check)"
	@echo "  run            Run the main demo script"
	@echo "  run-examples   Run all example scripts"
	@echo "  clean          Clean temporary files and artifacts"
	@echo "  docs           Generate documentation (if available)"
	@echo ""

# Installation
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

setup-dev: install
	@echo "Setting up development environment..."
	pip install pytest pytest-cov black flake8 mypy

# Testing
test:
	@echo "Running tests..."
	python -m pytest tests/ -v

test-verbose:
	@echo "Running tests with verbose output..."
	python -m pytest tests/ -v -s

test-coverage:
	@echo "Running tests with coverage..."
	python -m pytest tests/ --cov=. --cov-report=html --cov-report=term

# Code quality
lint:
	@echo "Running linting..."
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format:
	@echo "Formatting code..."
	black .
	@echo "Code formatting complete."

format-check:
	@echo "Checking code format..."
	black --check .

type-check:
	@echo "Running type checking..."
	mypy . --ignore-missing-imports

check-all: format-check lint type-check
	@echo "All quality checks completed."

# Running the application
run:
	@echo "Running main demo..."
	python main.py

run-examples:
	@echo "Running EPA analysis example..."
	python examples/epa_analysis_example.py
	@echo ""
	@echo "Running sales analysis example..."
	python examples/sales_analysis_example.py
	@echo ""
	@echo "Running validation examples..."
	python examples/validation_examples.py

# Individual examples
run-epa-example:
	@echo "Running EPA analysis example..."
	python examples/epa_analysis_example.py

run-sales-example:
	@echo "Running sales analysis example..."
	python examples/sales_analysis_example.py

run-validation-example:
	@echo "Running validation examples..."
	python examples/validation_examples.py

# Configuration
show-config:
	@echo "Current configuration:"
	python config.py

# Cleanup
clean:
	@echo "Cleaning temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	@echo "Cleanup complete."

# Development helpers
dev-setup: setup-dev
	@echo "Development environment setup complete."
	@echo "You can now run:"
	@echo "  make test      # Run tests"
	@echo "  make run       # Run the application"
	@echo "  make check-all # Run all quality checks"

# Git helpers
git-status:
	@echo "Git status:"
	git status

git-add:
	@echo "Adding all changes..."
	git add .

git-commit:
	@echo "Committing changes..."
	@if [ -z "$(message)" ]; then \
		echo "Usage: make git-commit message='Your commit message'"; \
		exit 1; \
	fi
	git commit -m "$(message)"

# Quick development cycle
dev-cycle: format test run
	@echo "Development cycle complete: formatted, tested, and ran application."

# CI/CD helpers
ci-test: test lint type-check
	@echo "CI testing complete."

# Documentation (placeholder for future docs)
docs:
	@echo "Documentation generation not yet implemented."
	@echo "Consider adding sphinx or mkdocs in the future."

# Project information
info:
	@echo "GDAPC-Dutta Data Analysis Project"
	@echo "=================================="
	@echo "Python version:"
	@python --version
	@echo ""
	@echo "Pip version:"
	@pip --version
	@echo ""
	@echo "Installed packages:"
	@pip list | grep -E "(pandas|numpy|pytest|black|flake8|mypy)" || echo "Dev packages not installed"