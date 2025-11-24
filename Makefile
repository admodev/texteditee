.PHONY: help install dev test lint format clean build-windows build-linux build-macos run

help:
	@echo "TextEditee - Makefile Commands"
	@echo "==============================="
	@echo "install       - Install dependencies"
	@echo "dev           - Install development dependencies"
	@echo "test          - Run tests"
	@echo "lint          - Run linters"
	@echo "format        - Format code"
	@echo "clean         - Clean build artifacts"
	@echo "build-windows - Build Windows executable"
	@echo "build-linux   - Build Linux executable"
	@echo "build-macos   - Build macOS executable"
	@echo "run           - Run the editor"

install:
	pip install -r requirements.txt

dev:
	pip install -r requirements.txt
	pip install pytest pytest-cov black mypy ruff pyinstaller

test:
	pytest tests/ -v --cov=src/texteditee

lint:
	ruff check src/
	mypy src/

format:
	black src/ tests/

clean:
	rm -rf build/ dist/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build-windows:
	cd installers && build_windows.bat

build-linux:
	cd installers && chmod +x build_linux.sh && ./build_linux.sh

build-macos:
	cd installers && chmod +x build_macos.sh && ./build_macos.sh

run:
	python -m src.texteditee.main
