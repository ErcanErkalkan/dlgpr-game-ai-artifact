FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["bash", "-lc", "python -m tests.run_tests && python scripts/run_full_validation.py --quick && python scripts/analyze_results.py && python scripts/make_manuscript_assets.py && python scripts/audit_package.py"]
