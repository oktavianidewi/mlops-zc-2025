import os
from datetime import datetime
from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from pendulum import datetime
import requests
from pathlib import Path

# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from src.pipeline.ingestion import ingestion_data


@dag(
    start_date=datetime(2024, 1, 1),
    schedule='*/10 * * * *',
    catchup=False,
    doc_md=__doc__,
    default_args={"owner": "Dewi", "retries": 3},
    tags=["ml_training"],
)

def generate_drift():
    generate_drift_task = BashOperator(
        task_id = "generate_drift_task",
        bash_command='python3 /opt/airflow/src/pipeline/generate_drift.py'
    )
    

    generate_drift_task

generate_drift()