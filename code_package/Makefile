PYTHON ?= python

.PHONY: test quick analyze manuscript sensitivity audit bundle all clean

test:
	$(PYTHON) -m tests.run_tests

quick:
	$(PYTHON) scripts/run_full_validation.py --quick

analyze:
	$(PYTHON) scripts/analyze_results.py

synthetic-manuscript:
	$(PYTHON) scripts/make_manuscript_assets.py

sensitivity:
	$(PYTHON) scripts/run_sensitivity.py
	$(PYTHON) scripts/analyze_sensitivity.py

audit:
	$(PYTHON) scripts/audit_package.py

bundle:
	$(PYTHON) scripts/make_submission_bundle.py

all: test quick analyze synthetic-manuscript sensitivity audit bundle

clean:
	rm -rf logs/full_validation logs/sensitivity paper/revised/tables paper/revised/figures paper/revised/manuscript_assets __pycache__ .pytest_cache
	find . -name "*.pyc" -delete
