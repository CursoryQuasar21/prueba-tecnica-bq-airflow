"""Technical test DAG for validating Airflow orchestration patterns."""

from __future__ import annotations

from datetime import datetime, timedelta
from datetime import timezone

from airflow import DAG
from airflow.operators.empty import EmptyOperator as DummyOperator

try:
    from plugins.operators.time_diff_operator import TimeDiffOperator
except ModuleNotFoundError:
    from operators.time_diff_operator import TimeDiffOperator


N_TASKS = 6

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(1900, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(seconds=5),
}

# Hook vs Connection:
# A Connection stores external system credentials and connection metadata in
# Airflow. A Hook is Python code that reads a Connection and exposes a reusable
# interface to interact with that external system. In short, Connections are
# configuration; Hooks are integration logic that uses that configuration.


with DAG(
    dag_id="test",
    description="Airflow DAG for the technical test dynamic task exercise.",
    default_args=default_args,
    schedule="0 3 * * *",
    catchup=False,
    tags=["data-engineering", "technical-test"],
) as dag:
    start = DummyOperator(task_id="start")
    end = DummyOperator(task_id="end")

    dynamic_tasks = [
        DummyOperator(task_id=f"task_{task_number}")
        for task_number in range(1, N_TASKS + 1)
    ]

    odd_tasks = [
        task
        for task_number, task in enumerate(dynamic_tasks, start=1)
        if task_number % 2 != 0
    ]
    even_tasks = [
        task
        for task_number, task in enumerate(dynamic_tasks, start=1)
        if task_number % 2 == 0
    ]

    time_diff = TimeDiffOperator(
        task_id="time_diff",
        diff_date=datetime(1900, 1, 1, tzinfo=timezone.utc),
    )

    start >> odd_tasks

    for even_task in even_tasks:
        odd_tasks >> even_task

    even_tasks >> time_diff >> end
