from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Import your ingestion functions
from ingestion.weather_ingestion import upload_all_cities_raw
from ingestion.silver_weather_to_blob import process_all_cities_to_silver
from ingestion.gold_load_azure_postgre import load_gold_for_all_cities

default_args = {
    "owner": "taz",
    "retries": 2,
    "retry_delay": timedelta(minutes=5)
}

with DAG(
    dag_id="weather_pipeline",
    default_args=default_args,
    start_date=datetime(2026, 8, 9),
    schedule_interval="0 * * * *",  # runs every hour
    catchup=False
):

    extract_raw = PythonOperator(
        task_id="extract_raw_weather",
        python_callable=upload_all_cities_raw
    )

    clean_silver = PythonOperator(
        task_id="clean_to_silver",
        python_callable=process_all_cities_to_silver
    )

    load_gold = PythonOperator(
        task_id="load_gold_to_postgres",
        python_callable=load_gold_for_all_cities
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/airflow/dbt && dbt run"
    )

    notify = BashOperator(
        task_id="notify_success",
        bash_command="echo 'Weather pipeline completed successfully!'"
    )

    extract_raw >> clean_silver >> load_gold >> dbt_run >> notify
