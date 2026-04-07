ifndef VERSION
	VERSION := $(shell git describe --tags --always --exclude latest)
endif
GIT_COMMIT := $(shell git rev-parse HEAD)

# Load environment variables from .env if it exists
ifneq (,$(wildcard .env))
    include .env
else
    $(info Warning: .env file not found, see .env.example for reference)
endif

# Setup python environment and install all packages
setup:
	uv sync --group dev

run-tests:
	uv run pytest

format:
	. .venv/bin/activate && \
	ruff format models/ tests/ scripts/