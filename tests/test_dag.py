﻿import os
import tempfile

# 1) Create a temp AIRFLOW_HOME and DB file
tmp_home = tempfile.mkdtemp(prefix="airflow_home_")
os.environ["AIRFLOW_HOME"] = tmp_home

# Use a real SQLite file for a shared DB
db_path = os.path.join(tmp_home, "airflow_test.db")
os.environ["AIRFLOW__CORE__SQL_ALCHEMY_CONN"] = f"sqlite:///{db_path}"

# Skip sync and examples
os.environ["AIRFLOW__CORE__UNIT_TEST_MODE"] = "True"
os.environ["AIRFLOW__CORE__LOAD_EXAMPLES"] = "False"

# 2) Bootstrap Airflow’s ORM and create tables on that file
from airflow import settings
from airflow.models.base import Base

settings.configure_orm()
Base.metadata.create_all(settings.engine)
