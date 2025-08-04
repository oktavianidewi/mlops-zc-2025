# https://www.youtube.com/watch?v=OLXkGB7krGo

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
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    doc_md=__doc__,
    default_args={"owner": "Dewi", "retries": 3},
    tags=["ml_training"],
)

def training_ml():
    ingestion = BashOperator(
        task_id = "ingestion_task",
        bash_command='python3 /opt/airflow/src/pipeline/ingestion.py'
    )
    
    split_data = BashOperator(
        task_id = "split_data_task",
        bash_command='python3 /opt/airflow/src/pipeline/split_data.py'

    )

    training = BashOperator(
        task_id = "training_task",
        bash_command='python3 /opt/airflow/src/pipeline/train.py'

    )

    ingestion >> split_data >> training
    
training_ml()