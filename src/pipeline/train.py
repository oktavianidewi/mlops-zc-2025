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
from split_data import split_data

mlflow.set_tracking_uri('http://host.docker.internal:5001')
mlflow.set_experiment('diabetes-experiment-mlflow')
parent_path = '/opt/airflow/src/pipeline/data'

# read from split data X_train, X_test, y_train, y_test
# X, X_train, X_test, y_train, y_test = split_data()

X = pd.read_csv(f'{parent_path}/X.csv')
X_train = pd.read_csv(f'{parent_path}/X_train.csv')
X_test = pd.read_csv(f'{parent_path}/X_test.csv')
y_train = pd.read_csv(f'{parent_path}/y_train.csv')
y_test = pd.read_csv(f'{parent_path}/y_test.csv')

numeric_features = X.columns
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

# build processing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features)
    ])

# build model pipeline
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=100))
])

# fit
pipeline.fit(X_train, y_train)

# make predictions
y_pred = pipeline.predict(X_test)
y_proba = pipeline.predict_proba(X_test)[:, 1]

# evaluate the model
acc = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_proba)

report = classification_report(y_test, y_pred)
print(f'Accuracy: {acc}')
print(f'Classification Report:\n{report}')

# checking if file exist and create artifacts file if none
artifact_file = 'artifacts/mlflow-diabetes.b'
create_folder_file('artifacts', 'mlflow-diabetes.b')

with mlflow.start_run() as run:
    mlflow.log_params(pipeline.named_steps['classifier'].get_params())
    mlflow.log_metrics(
        {
            'accuracy': acc,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'roc_auc': roc_auc,
        }
    )

    mlflow.log_artifact(artifact_file, artifact_path='preprocessor')
    mlflow.sklearn.log_model(
        sk_model=pipeline,
        name="rf-classifier-model",
        input_example=X_train,
        registered_model_name="rf-classifier-reg-model",
    )

    run_id = run.info.run_id
    print(run_id)