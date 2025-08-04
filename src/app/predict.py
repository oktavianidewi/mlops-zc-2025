import os
from pathlib import Path

import mlflow
import mlflow.sklearn
import pandas as pd
from mlflow.tracking import MlflowClient


mlflow.set_tracking_uri('http://host.docker.internal:5001')
# mlflow.set_tracking_uri('http://localhost:5001')
client = MlflowClient()

def list_models():
    print(f"HALO! {client.search_registered_models()}")
    for model in client.search_registered_models():
        print(f"{model.name}")

def __get_latest_model():
    list_models()
    latest_version = client.get_latest_versions('rf-classifier-reg-model')[0].version
    print(f"latest_version!! {latest_version}")
    model_uri = f"models:/rf-classifier-reg-model/{latest_version}"
    return model_uri

def load_model():
    '''Load the model from the MLflow model registry.'''
    # mlflow.set_tracking_uri('http://localhost:5001')
    # os.getenv("MLFLOW_TRACKING_URI")
    # config = read_yaml(Path("src/config/config.yaml"))
    # client = MlflowClient()
    # model_uri = f"models:/{config.model_registry.name}/{latest_version}"
    model_uri = __get_latest_model()
    model = mlflow.sklearn.load_model(model_uri)
    return model


def predict(input_data: dict):
    '''Predict churn based on input data.'''
    model = load_model()
    df = pd.DataFrame([input_data])
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]

    model_uri = __get_latest_model()
    return int(prediction), float(round(probability, 4)), model_uri
