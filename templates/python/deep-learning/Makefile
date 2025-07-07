# Makefile for deep learning project

.PHONY: help install dev test lint format type-check clean train evaluate setup

# Default target
help:
	@echo "Available commands:"
	@echo "  install     Install dependencies"
	@echo "  dev         Install development dependencies"
	@echo "  test        Run tests"
	@echo "  lint        Run linting"
	@echo "  format      Format code"
	@echo "  type-check  Run type checking"
	@echo "  clean       Clean cache and build files"
	@echo "  train       Run training with default config"
	@echo "  evaluate    Run evaluation (requires --checkpoint)"
	@echo "  setup       Setup pre-commit hooks"

# Installation
install:
	pip install -e .

dev:
	pip install -e ".[dev]"

# Code quality
test:
	pytest tests/ -v

lint:
	ruff check src/ tests/

format:
	ruff format src/ tests/

type-check:
	mypy src/

# Setup
setup:
	pre-commit install

# Cleaning
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf htmlcov/

# Training shortcuts
train:
	python train.py

train-cnn:
	python train.py --model-model-type cnn --training-max-epochs 50

train-transformer:
	python train.py --model-model-type transformer --training-max-epochs 50

train-hybrid:
	python train.py --model-model-type hybrid --training-max-epochs 50

# Evaluation
evaluate:
	@if [ -z "$(CHECKPOINT)" ]; then \
		echo "Error: Please provide a checkpoint path with CHECKPOINT=path/to/checkpoint.ckpt"; \
		exit 1; \
	fi
	python evaluate.py --checkpoint $(CHECKPOINT)