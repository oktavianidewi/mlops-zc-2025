import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
import pickle
import os
import mlflow

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.dir import create_folder_file

mlflow.set_tracking_uri('http://host.docker.internal:5001') # docker
# mlflow.set_tracking_uri('http://localhost:5001') # local
mlflow.set_experiment('diabetes-experiment-mlflow-drift')

# parent_path = '/opt/airflow/src/pipeline/data' # docker
parent_path = 'pipeline/data' # local

reference_data = pd.read_csv(f'{parent_path}/reference_data.csv')
new_data = pd.read_csv(f'{parent_path}/new_data.csv')

df= pd.concat([reference_data, new_data], ignore_index=True)

X = df.drop('Outcome', axis=1)
y = df['Outcome']

numeric_features = X.columns
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features)
    ])

pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))
])

pipeline.fit(X, y)

# checking if file exist and create artifacts file if none
artifact_file = 'artifacts/mlflow-diabetes-drift.b'
create_folder_file('artifacts', 'mlflow-diabetes-drift.b')

with mlflow.start_run() as run:
    mlflow.log_params(pipeline.named_steps['classifier'].get_params())
    mlflow.log_artifact(artifact_file, artifact_path='preprocessor')
    mlflow.sklearn.log_model(
        sk_model=pipeline,
        name="rf-classifier-model-drift",
        input_example=X,
        registered_model_name="rf-classifier-reg-model-drift",
    )

    run_id = run.info.run_id
    print(run_id)