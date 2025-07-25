import os
import tempfile

# ─── 1) Point Airflow at an in-memory DB and a temp home ────────────────────
tmp_home = tempfile.mkdtemp(prefix="airflow_home_")
os.environ["AIRFLOW_HOME"] = tmp_home
os.environ["AIRFLOW__CORE__SQL_ALCHEMY_CONN"] = "sqlite:///:memory:"
os.environ["AIRFLOW__CORE__UNIT_TEST_MODE"] = "True"
os.environ["AIRFLOW__CORE__LOAD_EXAMPLES"] = "False"

# ─── 2) Bootstrap Airflow’s ORM and create all tables immediately ─────────
from airflow import settings
from airflow.models.base import Base

settings.configure_orm()
Base.metadata.create_all(settings.engine)
