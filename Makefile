.PHONY: help setup data features stage0 stage1 gate stage2 inference figures test lint clean all
.DEFAULT_GOAL := help

PY ?= python

help:  ## Show this help
	@grep -E '^[a-z0-9-]+:.*?## ' $(MAKEFILE_LIST) | awk -F':.*?## ' '{printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

setup:  ## Create the conda environment
	conda env create -f environment.yml || conda env update -f environment.yml
	@echo "conda activate hfpos && pip install -e ."

data:  ## Ingest CFTC, prices and FRED into data/raw
	$(PY) -m hfpos.ingest.cftc
	$(PY) -m hfpos.ingest.prices
	$(PY) -m hfpos.ingest.fred

features: data  ## Build the modelling frame into data/processed
	$(PY) -m hfpos.features.build

stage0: features  ## Lead-lag and VAR: do positions lead or lag returns?
	$(PY) -m hfpos.stage0.leadlag

stage1: features  ## Walk-forward Stage 1; writes the positioning surprise
	$(PY) -m hfpos.stage1.run

gate: stage1  ## WEEK-5 GATE: Stage-1 OOS R2 and corr(residual, raw). Blocks Stage 2.
	@echo "Gate: report OOS R2 and corr(residual, raw d(Net/OI))."
	@echo "If that correlation exceeds ~0.9 the decomposition is cosmetic - stop and rethink scope."

stage2: stage1  ## Primary test plus the four definitions of 'unusual'
	$(PY) -m hfpos.stage2.predict

inference: stage2  ## Block bootstrap, Newey-West, multiplicity adjustment
	$(PY) -m hfpos.stage2.inference

figures:  ## Decomposition figure and result plots
	$(PY) -m hfpos.eval.plots

test:  ## Run the leakage and timing guards
	pytest -q

lint:  ## Ruff check
	ruff check src tests

clean:  ## Remove derived data and caches
	rm -rf data/interim/* data/processed/* reports/figures/* reports/tables/*
	find . -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null || true

all: test stage0 gate stage2 inference figures  ## Full pipeline
