import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Point to GCP key in container
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/opt/airflow/gcp_credentials.json"

default_args = {
    "owner": "Zweli",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="e_commerce_etl",
    default_args=default_args,
    description="ETL: store_sales + product_details → BigQuery",
    schedule_interval="0 2 * * *",
    start_date=datetime(2025, 7, 22),
    catchup=False,
    tags=["ecommerce", "bigquery"],
) as dag:

    def load_store_sales():
        import pandas as pd
        from google.cloud import bigquery

        df = pd.read_csv("/opt/airflow/data/store_sales.csv")
        client = bigquery.Client()
        table = f"{client.project}.ecommerce_staging.store_sales"
        client.load_table_from_dataframe(df, table).result()
        print("✅ store_sales loaded")

    def load_product_details():
        import pandas as pd
        from google.cloud import bigquery

        df = pd.read_json("/opt/airflow/data/product_details.json")
        client = bigquery.Client()
        table = f"{client.project}.ecommerce_staging.product_details"
        client.load_table_from_dataframe(df, table).result()
        print("✅ product_details loaded")

    task1 = PythonOperator(task_id="load_sales",    python_callable=load_store_sales)
    task2 = PythonOperator(task_id="load_products", python_callable=load_product_details)

    from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator

    sql = """
    CREATE OR REPLACE TABLE ecommerce_staging.transformed_sales_data AS
    SELECT
      s.date, s.store_id, s.product_id,
      p.product_name, LOWER(TRIM(p.category)) AS category,
      s.units_sold, s.sales_amount
    FROM ecommerce_staging.store_sales s
    JOIN ecommerce_staging.product_details p
      ON s.product_id = p.product_id;
    """
    task3 = BigQueryInsertJobOperator(
        task_id="transform", configuration={"query": {"query": sql, "useLegacySql": False}}
    )

    task1 >> task2 >> task3
