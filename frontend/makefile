SHELL := /bin/bash
NPM := npm

.PHONY: help install ci dev build test test-ci lint format clean

help:
	@echo ""
	@echo "Frontend Makefile targets (CRA / react-scripts):"
	@echo "  make install    Install dependencies"
	@echo "  make ci         Clean install (CI-style)"
	@echo "  make dev        Start dev server (npm start)"
	@echo "  make build      Production build"
	@echo "  make test       Run tests (interactive)"
	@echo "  make test-ci    Run tests once (CI=true)"
	@echo "  make lint       Run eslint on src/"
	@echo "  make format     Run prettier on src/"
	@echo "  make clean      Remove node_modules + build artifacts"
	@echo ""

install:
	$(NPM) install

ci:
	$(NPM) ci

dev:
	$(NPM) run start

build:
	$(NPM) run build

test:
	$(NPM) run test

test-ci:
	CI=true $(NPM) run test

lint:
	$(NPM) run lint

format:
	$(NPM) run format

clean:
	rm -rf node_modules build coverage
