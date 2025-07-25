#!/usr/bin/env bash
set -euo pipefail

# initialize DB only once
if [[ ! -f "${AIRFLOW_HOME}/airflow.db" ]]; then
  echo "[entrypoint] Initializing the Airflow DB…"
  airflow db init
fi

echo "[entrypoint] Starting the scheduler…"
exec airflow scheduler
