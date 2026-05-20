"""Airflow DAG placeholder for the technical test project.

TODO: Define the ingestion and transformation workflow.
"""

from __future__ import annotations

from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator


with DAG(
    dag_id="technical_test_pipeline",
    description="Placeholder DAG for the Data Engineering technical test.",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["data-engineering", "technical-test"],
) as dag:
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    start >> end
