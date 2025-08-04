import pandas as pd
from evidently.presets import DataDriftPreset
from evidently.core.report import Report
import json
import psycopg
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS evidently_reports_raw (
    timestamp TIMESTAMP NOT NULL,
    metric_id TEXT NOT NULL,
    value DOUBLE PRECISION
);
"""

def save_report_to_db(report: pd.DataFrame):
    logger.info("Saving report to database...")
    _prep_db()
    with _get_db_connection() as conn:
        with conn.cursor() as cur:
            for _, row in report.iterrows():
                cur.execute("""
                    INSERT INTO evidently_reports_raw (timestamp, metric_id, value)
                    VALUES (%s, %s, %s)
                """, (row.timestamp, row.metric_id, row.value))

            logger.info("Report successfully inserted into the database.")

def _get_db_connection(autocommit=True):
    
    # host = "localhost" # local
    host = "host.docker.internal" # docker

    logger.info("Connecting to PostgreSQL DB...")
    conn = psycopg.connect(
        host=os.getenv("PG_HOST", host),
        port=int(os.getenv("PG_PORT", "5432")),
        dbname=os.getenv("PG_DATABASE", "mlflow"),
        user=os.getenv("PG_USER", "mlflow"),
        password=os.getenv("PG_PASSWORD", "mlflow"),
        autocommit=autocommit,
    )
    logger.info("Connecting to PostgreSQL DB...")
    return conn

def _prep_db():
    logger.info("Preparing database and ensuring table exists...")
    with _get_db_connection() as conn:
        conn.execute(CREATE_TABLE_SQL)
        logger.info("Table `evidently_reports_raw` is ready.")


def detect_drift():
    # parent_path = 'pipeline/data' # local
    parent_path = '/opt/airflow/src/pipeline/data' # docker
    reference_data = pd.read_csv(f'{parent_path}/reference_data.csv')
    new_data = pd.read_csv(f'{parent_path}/new_data.csv')

    data_drift_report = Report(metrics=[
        DataDriftPreset()
    ])

    data_drift_result = data_drift_report.run(
        reference_data=reference_data.drop('Outcome', axis=1),
        current_data=new_data.drop('Outcome', axis=1)
    )

    report_json = json.loads(data_drift_result.json())

    ts = datetime.utcnow()
    report_df = pd.DataFrame(report_json['metrics'][1:])
    report_df['timestamp'] = ts
    print(report_df.head())

    save_report_to_db(report_df)

    drift_detected = report_json['metrics'][0]["value"]["count"] >= 1

    if drift_detected:
        print(json.dumps({"drift_detected": True}))
    else:
        print(json.dumps({"drift_detected": False}))

detect_drift()