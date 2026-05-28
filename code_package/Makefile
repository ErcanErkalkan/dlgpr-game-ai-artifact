PYTHON ?= python

.PHONY: test quick analyze manuscript external external-analyze timing timing-analyze sensitivity audit audit-release bundle all clean

test:
	$(PYTHON) -m tests.run_tests

quick:
	$(PYTHON) scripts/run_full_validation.py --quick

analyze:
	$(PYTHON) scripts/analyze_results.py

synthetic-manuscript:
	$(PYTHON) scripts/make_manuscript_assets.py

external:
	$(PYTHON) scripts/run_external_validation.py --full

external-analyze:
	$(PYTHON) scripts/analyze_results.py --log-dir ../experiments/tog2026_external_gymnasium/logs/external_validation --table-dir ../experiments/tog2026_external_gymnasium/paper/revised/tables --fig-dir ../experiments/tog2026_external_gymnasium/paper/revised/figures

timing:
	$(PYTHON) scripts/run_timing_profile.py --full

timing-analyze:
	$(PYTHON) scripts/analyze_results.py --log-dir ../experiments/tog2026_timing_profile/logs/timing_profile --table-dir ../experiments/tog2026_timing_profile/paper/revised/tables --fig-dir ../experiments/tog2026_timing_profile/paper/revised/figures

sensitivity:
	$(PYTHON) scripts/run_sensitivity.py
	$(PYTHON) scripts/analyze_sensitivity.py

audit:
	$(PYTHON) scripts/audit_package.py

audit-release:
	$(PYTHON) scripts/audit_package.py --log-dir ../experiments/tog2026_full_validation/logs/full_validation --table-dir ../experiments/tog2026_full_validation/paper/revised/tables
	$(PYTHON) scripts/audit_package.py --log-dir ../experiments/tog2026_external_gymnasium/logs/external_validation --table-dir ../experiments/tog2026_external_gymnasium/paper/revised/tables
	$(PYTHON) scripts/audit_package.py --log-dir ../experiments/tog2026_timing_profile/logs/timing_profile --table-dir ../experiments/tog2026_timing_profile/paper/revised/tables

bundle:
	$(PYTHON) scripts/make_submission_bundle.py

all: test quick analyze synthetic-manuscript sensitivity audit bundle

clean:
	rm -rf logs/full_validation logs/sensitivity paper/revised/tables paper/revised/figures paper/revised/manuscript_assets __pycache__ .pytest_cache
	find . -name "*.pyc" -delete
