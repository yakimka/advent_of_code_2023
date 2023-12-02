SHELL:=/usr/bin/env bash

setup-venv:
	@if [ -d ".venv" ]; then \
		echo "Error: .venv directory already exists"; \
		exit 1; \
	fi
	@echo "Setting up virtual environment..."
	@python3 -m venv .venv
	@echo "Installing dependencies..."
	@.venv/bin/pip install pre-commit==3.5.0 ipython pytest
	@echo "Done."

new-day:
	@if [ -z "$(day)" ]; then \
		echo "Error: day is required"; \
		exit 1; \
	fi
	@if [ -d "day$(day)" ]; then \
		echo "Error: day$(day) directory already exists"; \
		exit 1; \
	fi
	@echo "Creating day$(day) directory..."
	@cp -r day00 day$(day)

lint:
	@.venv/bin/pre-commit run --all-files

test:
	@for num in `seq -w 1 31`; do \
		day="day$$num"; \
		if [ -d "$$day" ]; then \
			echo "Testing in $$day"; \
			(cd $$day; pytest part*.py); \
		fi \
	done
