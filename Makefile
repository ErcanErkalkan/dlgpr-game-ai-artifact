PYTHON ?= python

.PHONY: install test quick analyze manuscript external external-analyze timing timing-analyze sensitivity audit audit-release bundle all clean

install:
	$(PYTHON) -m pip install -e .

test:
	$(PYTHON) code_package/tests/run_tests.py

quick:
	$(PYTHON) code_package/scripts/run_full_validation.py --quick

analyze:
	$(PYTHON) code_package/scripts/analyze_results.py --log-dir code_package/logs/full_validation --table-dir code_package/paper/revised/tables --fig-dir code_package/paper/revised/figures

synthetic-manuscript:
	$(PYTHON) code_package/scripts/make_manuscript_assets.py

external:
	$(PYTHON) code_package/scripts/run_external_validation.py --full

external-analyze:
	$(PYTHON) code_package/scripts/analyze_results.py --log-dir experiments/tog2026_external_gymnasium/logs/external_validation --table-dir experiments/tog2026_external_gymnasium/paper/revised/tables --fig-dir experiments/tog2026_external_gymnasium/paper/revised/figures

timing:
	$(PYTHON) code_package/scripts/run_timing_profile.py --full

timing-analyze:
	$(PYTHON) code_package/scripts/analyze_results.py --log-dir experiments/tog2026_timing_profile/logs/timing_profile --table-dir experiments/tog2026_timing_profile/paper/revised/tables --fig-dir experiments/tog2026_timing_profile/paper/revised/figures

sensitivity:
	$(PYTHON) code_package/scripts/run_sensitivity.py
	$(PYTHON) code_package/scripts/analyze_sensitivity.py

audit:
	$(PYTHON) code_package/scripts/audit_package.py --profile full --out experiments/tog2026_full_validation/PACKAGE_AUDIT_REPORT.md
	$(PYTHON) code_package/scripts/audit_package.py --profile external --log-dir experiments/tog2026_external_gymnasium/logs/external_validation --table-dir experiments/tog2026_external_gymnasium/paper/revised/tables --out experiments/tog2026_external_gymnasium/PACKAGE_AUDIT_REPORT.md
	$(PYTHON) code_package/scripts/audit_package.py --profile timing --log-dir experiments/tog2026_timing_profile/logs/timing_profile --table-dir experiments/tog2026_timing_profile/paper/revised/tables --out experiments/tog2026_timing_profile/PACKAGE_AUDIT_REPORT.md

audit-release: audit

bundle:
	$(PYTHON) code_package/scripts/make_submission_bundle.py

all: test quick analyze synthetic-manuscript sensitivity audit bundle

clean:
	rm -rf code_package/logs/full_validation code_package/logs/sensitivity code_package/paper/revised/tables code_package/paper/revised/figures code_package/paper/revised/manuscript_assets __pycache__ .pytest_cache *.egg-info code_package/*.egg-info
	find . -name "*.pyc" -delete
