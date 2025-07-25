#!/usr/bin/env python3
import os
from pathlib import Path

# 1. Define paths
root = Path(__file__).parent.resolve()
workflow_dir = root / ".github" / "workflows"
workflow_file = workflow_dir / "ci-cd.yml"

# 2. Ensure directory exists
workflow_dir.mkdir(parents=True, exist_ok=True)

# 3. CI/CD YAML template
ci_cd_yaml = """\
name: CI/CD for Airflow ETL

on:
  pull_request:
    branches: [ main ]
  push:
    branches: [ staging, main ]

jobs:

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: 3.11
      - name: Install dev dependencies
        run: |
          pip install --upgrade pip flake8
      - name: Run flake8
        run: flake8 airflow/dags

  test:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: 3.11
      - name: Install test dependencies
        run: pip install pytest -r requirements.txt
      - name: Run pytest
        run: pytest

  build:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: docker build -t my-etl-image .

  deploy:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - uses: actions/checkout@v3
      - name: Authenticate with GCP
        uses: google-github-actions/auth@v1
        with:
          credentials_json: ${{ secrets.GCP_CREDENTIALS }}
      - name: Push image to Container Registry
        run: |
          docker tag my-etl-image gcr.io/$GCP_PROJECT_ID/my-etl-image:latest
          docker push gcr.io/$GCP_PROJECT_ID/my-etl-image:latest
      # Add your deployment commands here
"""

# 4. Write to file
with open(workflow_file, "w") as f:
    f.write(ci_cd_yaml)

print(f"Created {workflow_file}")
