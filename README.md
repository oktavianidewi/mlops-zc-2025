# MLOps Pipeline for Diabetes Prediction with Drift Detection Simulation — MLOps Zoomcamp

## 📌 Project Description

This project implements a **machine learning pipeline** for training and monitoring models with **data drift detection simulation**.
The pipeline is orchestrated with **Apache Airflow**, logs experiments to **MLflow**, stores artifacts in **MinIO (S3-compatible)**, and saves drift metrics to **PostgreSQL**, making them accessible via **Grafana dashboards**. 

This project showcases a complete MLOps simulation running inside a Dockerized environment. It demonstrates how machine learning workflows—such as data ingestion, model training, drift detection, and retraining—can be seamlessly orchestrated using tools like Airflow, MLflow, and PostgreSQL.

The project leverages the Pima Indians Diabetes dataset, an open-source dataset provided by UCI Machine Learning Repository, which is also available on Kaggle: https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database

---

## ⚡ Problem Statement

In traditional ML workflows, collaboration between Data Engineers and Data Scientists often introduces delays and friction in productionizing models:

**From a Data Engineer’s Perspective**
- Porting ML changes into production pipelines takes significant time because:
    - Manual integration of new model artifacts and dependencies.
    - Coordination with data scientists for retraining and feature changes.
- Without MLOps practices, deployment can take up to 1 week, causing operational bottlenecks.
- By adopting Airflow + MLflow + CI/CD, deployment time can be reduced to 1 day or less, significantly improving agility.

**From a Data Scientist’s Perspective**
- After training a new model, handing it over to engineers often involves:
    - Repeated alignment on input schema and preprocessing steps.
    - Uncertainty about how the model performs in production.

- Lack of automated drift detection can lead to:
    - Models silently degrading in production.
    - Late discovery of performance issues.

- With drift monitoring + experiment tracking, data scientists gain:
    - Faster model iteration cycles.
    - Clear visibility into model performance over time.

This problem motivates the implementation of a unified MLOps pipeline that bridges the gap between Data Engineers and Data Scientists, improving deployment speed, reliability, and monitoring.

This project addresses:

1. Automated **ETL & model training** workflow.
2. **Simulation of data drift detection** using Evidently AI.
3. **Experiment tracking and model versioning** using MLflow.
4. **Infrastructure reproducibility** using Docker.

---

## 🛠 Technology Stack

* **Python 3.10**
* **Docker**
* **Airflow 3.x** (orchestration)
* **MLflow** (experiment tracking)
* **Streamlit** (simple web app for diabetes prediction)
* **Evidently AI** (data drift detection)
* **MinIO** (S3 artifact storage)
* **PostgreSQL** (metadata & drift logging)
* **Grafana** (drift visualization)

---

## 🚀 Installation & Setup

### **1. Clone the Repository**

```bash
git clone https://github.com/oktavianidewi/mlops-zc-2025.git
cd mlops-zc-2025
```

### **2. Start Services with Docker Compose**

```bash
docker compose --env-file config.env up
```

This starts:

* Airflow Scheduler, Webserver, Triggerer, and API
* PostgreSQL
* MinIO (S3 storage for MLflow)
* MLflow tracking server
* Streamlit
* Grafana

---

### **3. Initialize Airflow**

```bash
docker compose --env-file config.env up airflow-init -d
```

---

### **4. Access Services**

* **Airflow UI** → [http://localhost:8080](http://localhost:8080)
```
username: airflow
password: airflow
```
* **MLflow UI** → [http://localhost:5000](http://localhost:5000)

* **MinIO Console** → [http://localhost:9001](http://localhost:9001)
```
username: minio_user
password: minio_pwd
```

* **Streamlit** → [http://localhost:8501](http://localhost:8505)
* **Grafana** → [http://localhost:3000](http://localhost:3000)
```
username: admin
password: admin
```

---

### **5. Run Your Pipeline**

**a. Model Training in Airflow**

The ML pipeline is orchestrated using Apache Airflow, where the model is trained as part of an automated DAG (Directed Acyclic Graph).


![](./images/a.%20train-model-airflow.png)



![](./images/a.%20train-model-airflow-detail.png)



![](./images/a.%20prediction.png)

**b. Experiment Tracking with MLflow**

All model runs, metrics, and artifacts are logged and tracked in MLflow, making it easier to compare different experiments and monitor model performance over time.

![](./images/b.%20experiment-tracking-mlflow.png)



![](./images/a.%20train-model-airflow-detail.png)


**c. Data Drift Simulation**

To emulate real-world scenarios where incoming data changes over time, data drift is simulated every 10 minutes.

![](./images/c.%20simulate-drift.png)



**d. Visualizing Drift in Grafana**

Drift metrics and monitoring data are pushed to PostgreSQL, and Grafana dashboards visualize the model’s performance and detected drifts.

![](./images/d.%20drift-in-grafana.png)



![](./images/d.%20grafana-with-pg-details.png)

**e. Automated Model Retraining**

When a drift is detected, the pipeline automatically triggers a model retraining step to ensure the model remains accurate on the latest data.

![](./images/e.%20retrain-when-drift.png)


---

## ✅ Features

* Automated **ML workflow** in Airflow.
* **Data drift detection** & metrics logging.
* **Experiment tracking & model registry** with MLflow.
* **Drift visualization** in Grafana.
* **Diabetes Prediction** in Streamlit.