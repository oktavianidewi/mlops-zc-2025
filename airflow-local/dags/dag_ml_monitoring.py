from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
import pandas as pd
from sklearn.metrics import accuracy_score
import random
import json

# ===== Helper Functions =====
def decide_branch(**context):
    drift_detected_xcom = context['ti'].xcom_pull(task_ids='detect_drift')
    drift_detected = json.loads(drift_detected_xcom)['drift_detected']
    if drift_detected == True:
        print("Branching to retraining pipeline, based on drift detection.")
        return "retrain_model"
    else:
        print("Branching to skip retraining, based on drift detection.")
        return "skip_retrain"

def retrain_model():
    # Dummy training
    print("Retraining model...done.")

def skip_retrain():
    print("No drift detected, skipping retraining.")

def evaluate_model():
    print("Evaluating model after branch step.")


# ===== DAG Definition =====
with DAG(
    dag_id="drift_detection_dag",
    start_date=datetime(2025, 1, 1),
    schedule="*/17 * * * *",
    catchup=False,
    default_args={"owner": "Dewi", "retries": 3},
    doc_md=__doc__,
    description="A DAG to detect data drift and conditionally retrain the model.",
    tags=["ml_training", "drift"]
) as dag:

    detect_drift_task = BashOperator(
        task_id="detect_drift",
        bash_command="python3 /opt/airflow/src/pipeline/monitor_drift.py",
        do_xcom_push=True
    )

    branch_task = BranchPythonOperator(
        task_id="branch_decision",
        python_callable=decide_branch,
    )

    retrain_task = BashOperator(
        task_id="retrain_model",
        bash_command="python3 /opt/airflow/src/pipeline/train_with_drift.py",
    )

    skip_task = PythonOperator(
        task_id="skip_retrain",
        python_callable=skip_retrain,
    )

    evaluate_task = PythonOperator(
        task_id="evaluate_model",
        python_callable=evaluate_model,
        trigger_rule="none_skipped"  # wait for whichever branch finishes
    )

    # DAG Dependencies
    detect_drift_task >> branch_task
    branch_task >> [retrain_task, skip_task]
    [retrain_task, skip_task] >> evaluate_task
