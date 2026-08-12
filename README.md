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

## 📋 Prerequisites

### **System Requirements**
- **CPU:** At least 4 cores recommended
- **RAM:** Minimum 8GB (16GB+ recommended for smooth operation)
- **Disk Space:** At least 10GB free
- **OS:** Windows 10/11, macOS, or Linux

### **Windows-Specific Setup**

#### **Option 1: Docker Desktop (Recommended for Windows)**
1. **Install Docker Desktop for Windows**
   - Download from: https://www.docker.com/products/docker-desktop
   - During installation, **enable WSL 2** (Windows Subsystem for Linux 2) when prompted
   - This is required for optimal Docker performance on Windows

2. **Enable WSL 2**
   - If not enabled during Docker Desktop setup:
     ```powershell
     # Run PowerShell as Administrator
     wsl --install
     wsl --set-default-version 2
     ```
   - Restart your computer after installation

3. **Verify Docker Installation**
   ```powershell
   docker --version
   docker-compose --version
   ```

#### **Option 2: Git Bash (Alternative for Windows)**
- If you prefer command-line tools similar to Linux, install **Git Bash**
- Download from: https://git-scm.com/download/win
- All commands in this guide can be run from Git Bash using bash syntax

### **macOS/Linux Prerequisites**
- Install Docker: https://docs.docker.com/engine/install/
- Ensure `docker` and `docker-compose` are installed and running

### **Common Prerequisites (All Platforms)**
- **Git** (https://git-scm.com/)
- **Python 3.10+** (optional, only if running pipeline steps outside Docker)
- **Text Editor or IDE** (VS Code, PyCharm, etc.)

---

## 🚀 Installation & Setup

### **1. Clone the Repository**

**Windows (PowerShell):**
```powershell
git clone https://github.com/oktavianidewi/mlops-zc-2025.git
cd mlops-zc-2025
```

**Windows (Git Bash):**
```bash
git clone https://github.com/oktavianidewi/mlops-zc-2025.git
cd mlops-zc-2025
```

**macOS/Linux:**
```bash
git clone https://github.com/oktavianidewi/mlops-zc-2025.git
cd mlops-zc-2025
```

### **2. Configure Environment Variables**

1. Open `config.env` in your text editor
2. Review default values:
   ```env
   AIRFLOW_CORE_EXECUTOR=LocalExecutor
   AIRFLOW_DATABASE_SQL_ALCHEMY_CONN=postgresql://airflow:airflow@postgres:5432/airflow
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=airflow
   MINIO_ROOT_USER=minio_user
   MINIO_ROOT_PASSWORD=minio_pwd
   MLFLOW_TRACKING_URI=http://mlflow:5000
   ```
3. (Optional) Modify credentials for production use
4. Save the file

### **3. Verify Docker is Running**

**Windows (PowerShell):**
```powershell
docker ps
```

**Expected Output:**
```
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

> **If you get an error:** Ensure Docker Desktop is running. Click the Docker icon in your system tray.

### **4. Start Services with Docker Compose**

**Windows (PowerShell):**
```powershell
# Navigate to project directory if not already there
cd path\to\mlops-zc-2025

# Log in to Docker (if needed for private repos)
docker login

# Start all services
docker compose --env-file config.env up -d
```

**Windows (Git Bash):**
```bash
cd path/to/mlops-zc-2025
docker login
docker compose --env-file config.env up -d
```

**macOS/Linux:**
```bash
cd mlops-zc-2025
docker login
docker compose --env-file config.env up
```

> **Note:** The `-d` flag runs containers in the background (detached mode). Remove it if you want to see logs in real-time.

This docker command will pull images, download and start these services:
- Airflow Scheduler, Webserver, Triggerer, and API
- PostgreSQL
- MinIO (S3 storage for MLflow)
- MLflow tracking server
- Streamlit
- Grafana

**Installation Duration:** Typically 5-10 minutes (depends on internet speed and system specs)

### **5. Monitor Container Status**

**Windows (PowerShell):**
```powershell
# Check all running containers
docker ps

# View logs from a specific service
docker compose logs airflow-webserver

# Follow logs in real-time
docker compose logs -f airflow-webserver
```

**Alternatively, use Docker Desktop GUI:**
- Open Docker Desktop → Containers tab
- You should see all services running with a green status indicator

![](./images/mlops-zc-docker-install.png)

---

## ✅ Quick Start Checklist (Windows)

Use this checklist to verify your setup is complete:

- [ ] Docker Desktop installed and running
- [ ] WSL 2 enabled (`wsl --version` shows v2)
- [ ] Git installed and working
- [ ] Repository cloned to your local machine
- [ ] `config.env` file exists in project root
- [ ] `docker compose ps` shows all containers running
- [ ] Can access Airflow UI at `http://localhost:8080`
- [ ] Can access MLflow UI at `http://localhost:5000`
- [ ] Can access MinIO at `http://localhost:9001`
- [ ] Can access Grafana at `http://localhost:3000`
- [ ] Can access Streamlit at `http://localhost:8501`
- [ ] PostgreSQL responsive: `docker compose exec postgres psql -U postgres -c "SELECT 1;"`
- [ ] Ready to trigger first DAG!

**Stuck?** Check the [Troubleshooting](#-troubleshooting) section for solutions.

---

### **6. Access Services**

Once all containers are running, open these URLs in your web browser:

| Service | URL | Username | Password |
|---------|-----|----------|----------|
| **Airflow UI** | [http://localhost:8080](http://localhost:8080) | airflow | airflow |
| **MLflow UI** | [http://localhost:5000](http://localhost:5000) | — | — |
| **MinIO Console** | [http://localhost:9001](http://localhost:9001) | minio_user | minio_pwd |
| **Streamlit App** | [http://localhost:8501](http://localhost:8501) | — | — |
| **Grafana** | [http://localhost:3000](http://localhost:3000) | admin | admin |

> **Troubleshooting:** If a URL doesn't respond, check container status with `docker ps` or `docker compose ps`

---

### **7. Verify All Services Are Ready (Windows)**

**PowerShell Script to Check All Services:**
```powershell
# Wait for services to be fully ready
Write-Host "Checking service availability..."

$services = @{
    "Airflow" = "http://localhost:8080"
    "MLflow" = "http://localhost:5000"
    "MinIO" = "http://localhost:9001"
    "Streamlit" = "http://localhost:8501"
    "Grafana" = "http://localhost:3000"
}

foreach ($service in $services.GetEnumerator()) {
    try {
        $response = Invoke-WebRequest -Uri $service.Value -TimeoutSec 5 -ErrorAction Stop
        Write-Host "✓ $($service.Name) is UP" -ForegroundColor Green
    } catch {
        Write-Host "✗ $($service.Name) is DOWN" -ForegroundColor Red
    }
}
```

---

### **8. Run Your Pipeline**

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

---

## 📁 Project Structure

```
mlops-zc-2025/
├── airflow-local/                  # Airflow DAGs directory
│   └── dags/
│       ├── dag_ml_training.py       # Main training DAG
│       ├── dag_generate_drift.py    # Drift simulation DAG
│       └── dag_ml_monitoring.py     # Monitoring & retraining DAG
├── src/
│   ├── pipeline/                    # Core ML pipeline logic
│   │   ├── ingestion.py             # Data ingestion from CSV
│   │   ├── split_data.py            # Train/test split
│   │   ├── train.py                 # Model training
│   │   ├── generate_drift.py        # Drift data generation
│   │   └── monitor_drift.py         # Drift detection logic
│   ├── app/                         # Streamlit prediction app
│   │   ├── app.py                   # Main Streamlit interface
│   │   └── predict.py               # Prediction logic
│   └── utils/                       # Utilities
│       └── dir.py                   # Directory management
├── docker-compose.yml               # Multi-container orchestration
├── config.env                       # Environment configuration
└── README.md                        # This file
```

---

## 🏗 Architecture Overview

```
Data Source (CSV)
       ↓
[Ingestion] → PostgreSQL (raw data)
       ↓
[Feature Eng & Split] → Train/Test sets
       ↓
[Model Training] → MLflow (metrics/artifacts)
                 → MinIO (model binary)
                 → PostgreSQL (model meta)
       ↓
[Prediction Service] ← Streamlit App
       ↓
[Drift Monitoring] → PostgreSQL (drift metrics)
                   → Grafana (visualization)
       ↓
[Automated Retraining] (when drift detected)
```

### Component Responsibilities

| Component | Role |
|-----------|------|
| **Airflow** | Orchestrates DAG scheduling; triggers training & monitoring tasks on schedule |
| **PostgreSQL** | Stores raw data, model metadata, drift metrics, and logs |
| **MLflow** | Logs model parameters, metrics, and artifacts; provides experiment UI |
| **MinIO** | S3-compatible storage for model binaries and training artifacts |
| **Grafana** | Visualizes drift metrics and model performance dashboards |
| **Streamlit** | Provides user-facing interface for real-time diabetes predictions |

---

## ⚙️ Configuration

The `config.env` file contains all environment variables for the Docker Compose setup:

```env
# Example config.env
AIRFLOW_CORE_EXECUTOR=LocalExecutor
AIRFLOW_DATABASE_SQL_ALCHEMY_CONN=postgresql://airflow:airflow@postgres:5432/airflow

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=airflow

MINIO_ROOT_USER=minio_user
MINIO_ROOT_PASSWORD=minio_pwd

MLFLOW_TRACKING_URI=http://mlflow:5000
```

**Key Configurable Parameters:**
- `AIRFLOW_CORE_EXECUTOR`: Can switch to `CeleryExecutor` for distributed tasks
- `POSTGRES_*`: Database credentials (change for production)
- `MINIO_*`: MinIO authentication (change for production)

---

## 🛠️ Development & Debugging (Windows)

### **Editing DAG Files**

1. **Locate DAG files:**
   ```
   airflow-local/dags/
   ├── dag_ml_training.py
   ├── dag_generate_drift.py
   └── dag_ml_monitoring.py
   ```

2. **Edit and save files** in your favorite editor (VS Code, PyCharm, etc.)

3. **Changes take effect automatically:**
   - Airflow scheduler automatically detects new/modified DAGs
   - No need to restart containers
   - Wait 30-60 seconds for changes to appear in Airflow UI

### **Running Commands Inside Containers**

**Execute commands in a container (Windows PowerShell):**
```powershell
# Example: Check Python version in Airflow container
docker compose exec airflow-webserver python --version

# Run a Python script
docker compose exec airflow-webserver python /your/script/path.py

# Run bash commands
docker compose exec airflow-webserver bash -c "command here"
```

### **Debugging with Logs**

**View specific service logs (Windows PowerShell):**
```powershell
# Follow Airflow logs in real-time
docker compose logs -f airflow-webserver

# View logs from last 100 lines
docker compose logs --tail=100 airflow-webserver

# View logs from specific time (ISO 8601 format)
docker compose logs --since 2025-08-12T14:30:00 airflow-webserver

# View logs from multiple services
docker compose logs -f airflow-webserver postgres mlflow
```

### **Accessing Python Environment in Containers**

**Interactive Python shell in Airflow container:**
```powershell
docker compose exec airflow-webserver python

# Inside Python:
>>> import sys
>>> print(sys.version)
>>> exit()
```

**Install Python packages temporarily (for testing):**
```powershell
# Install a package in running container
docker compose exec airflow-webserver pip install requests

# NOTE: Changes are lost when container restarts
# For permanent changes, modify Dockerfile or requirements.txt
```

### **Restart Strategies**

**Restart a single service:**
```powershell
docker compose restart airflow-webserver
```

**Restart all services:**
```powershell
docker compose restart
```

**Full reset (remove containers, keep volumes):**
```powershell
docker compose down
docker compose --env-file config.env up -d
```

### **Testing DAG Without Airflow Scheduler**

**Test Python syntax of a DAG:**
```powershell
# Check if DAG file has syntax errors
docker compose exec airflow-webserver python -m py_compile airflow-local/dags/dag_ml_training.py
```

**Parse DAG in Airflow:**
```powershell
# Validate DAG parsing
docker compose exec airflow-webserver airflow dags list-import-errors
```

### **Profiling & Resource Monitoring**

**Monitor resource usage in real-time (Windows PowerShell):**
```powershell
docker stats

# Press Ctrl+C to stop monitoring
```

**Save stats to file:**
```powershell
docker stats --no-stream > docker_stats.txt
```

**Check disk usage by containers:**
```powershell
docker system df
```

### **Cleaning Up Docker Artifacts (Safely)**

```powershell
# Remove unused images
docker image prune -a

# Remove unused volumes (WARNING: Deletes data!)
docker volume prune

# Remove unused networks
docker network prune

# Full cleanup (remove everything unused, keeps your running containers)
docker system prune
```

---

## 🔄 DAG Workflows

### **dag_ml_training.py**
- **Schedule:** Daily (configurable)
- **Steps:**
  1. Load diabetes dataset from CSV
  2. Split data into train/test sets
  3. Train logistic regression model
  4. Log metrics and model to MLflow
  5. Store model binary in MinIO
  6. Save model metadata to PostgreSQL

### **dag_generate_drift.py**
- **Schedule:** Every 10 minutes
- **Purpose:** Simulates real-world data drift by:
  1. Generating synthetic data with shifted feature distributions
  2. Saving to PostgreSQL for monitoring
  3. Triggering drift detection workflow

### **dag_ml_monitoring.py**
- **Schedule:** Every 10 minutes
- **Steps:**
  1. Fetch latest data from PostgreSQL
  2. Load latest model from MinIO
  3. Run Evidently AI drift detection
  4. Log drift metrics to PostgreSQL
  5. Trigger retraining if drift threshold exceeded

---

## 📊 Monitoring & Metrics

### Drift Detection Metrics
The system tracks the following metrics for each monitoring cycle:

- **Data Drift Score:** Detects feature distribution shifts
- **Prediction Drift:** Monitors changes in model predictions
- **Model Performance:** Tracks accuracy on recent data
- **Feature Statistics:** Min, max, mean, std dev per feature

### Grafana Dashboards
Access Grafana at `http://localhost:3000` to view:
- **Model Performance Over Time:** Accuracy, precision, recall trends
- **Drift Detection Status:** Visual alerts for detected drift
- **Feature Distribution Changes:** Before/after comparisons
- **Retraining Events:** When and why models were retrained

---

## 🔧 Usage Examples

### **Training a Model Manually**

**Via Airflow UI (Recommended):**
1. Go to `http://localhost:8080`
2. Log in with `airflow` / `airflow`
3. Find `dag_ml_training` in the DAG list
4. Click the DAG → Click the **play button** (▶) on the right
5. Select "Trigger DAG" in the popup
6. Monitor execution in the DAG runs section

**Via Command Line:**
```bash
# From project directory
docker compose exec airflow-webserver airflow dags trigger dag_ml_training
```

### **Making Predictions via Streamlit**

1. Open `http://localhost:8501` in your browser
2. You'll see a form with diabetes patient data fields:
   - Pregnancies
   - Glucose
   - Blood Pressure
   - Skin Thickness
   - Insulin
   - BMI
   - Diabetes Pedigree Function
   - Age
3. Enter values and click "Predict"
4. View real-time prediction with confidence score

### **Checking Model Experiments in MLflow**

1. Go to `http://localhost:5000`
2. Browse all training runs and metrics
3. Compare experiments side-by-side
4. Click on a run to see:
   - Model parameters
   - Training metrics (accuracy, precision, recall, etc.)
   - Model artifacts and files
5. Download trained models for external use

### **Querying Drift Metrics from PostgreSQL**

**Method 1: Connect via Docker Compose (Windows PowerShell)**
```powershell
# Connect to PostgreSQL inside container
docker compose exec postgres psql -U postgres -d airflow

# Inside psql shell, run queries:
postgres=# SELECT * FROM drift_metrics ORDER BY timestamp DESC LIMIT 10;
postgres=# SELECT COUNT(*) FROM drift_metrics;
postgres=# SELECT AVG(drift_score) FROM drift_metrics;
postgres=# \q  # Exit psql
```

**Method 2: Use External PostgreSQL Client (e.g., pgAdmin)**
1. Open `pgAdmin` (if available in docker-compose)
2. Add server with:
   - Host: `localhost`
   - Port: `5432`
   - Username: `postgres`
   - Password: `postgres`
   - Database: `airflow`
3. Query `drift_metrics` table

**Method 3: Direct SQL Query from Command Line (Windows PowerShell)**
```powershell
# Run single query without interactive shell
docker compose exec postgres psql -U postgres -d airflow -c "SELECT * FROM drift_metrics LIMIT 10;"
```

### **Monitoring Pipeline Execution**

**View Container Logs (Windows PowerShell):**
```powershell
# Tail Airflow scheduler logs
docker compose logs -f airflow-scheduler

# Tail MLflow logs
docker compose logs -f mlflow

# Tail all services
docker compose logs -f

# View logs from specific time
docker compose logs --since 2025-08-12T10:00:00
```

**Using Docker Desktop GUI (Visual Monitoring):**
1. Open Docker Desktop application
2. Go to Containers tab
3. Click on running containers to see:
   - Live logs
   - Resource usage (CPU, memory)
   - Network information
   - Mounted volumes

### **Stopping Services**

**Without removing data (pause):**
```powershell
docker compose stop
```

**Remove containers but keep volumes:**
```powershell
docker compose down
```

**Remove everything (including data!):**
```powershell
docker compose down -v  # WARNING: Deletes all data
```

**Restart a specific service:**
```powershell
docker compose restart airflow-webserver
```

### **View Container Statistics**

**Real-time resource usage:**
```powershell
docker stats

# For specific container
docker stats mlflow
```

---

## 🐛 Troubleshooting

### **Windows-Specific Issues**

#### **Issue: WSL 2 Not Installed or Docker Fails to Start**
- **Symptom:** "Docker is not installed" or containers won't start
- **Solution:**
  1. Open PowerShell as Administrator
  2. Run: `wsl --install`
  3. Restart your computer
  4. Reopen Docker Desktop
  5. Verify with: `docker ps`

#### **Issue: "The system cannot find the path specified" (Windows Paths)**
- **Symptom:** Error when running `docker compose up`
- **Cause:** Path separators (`\` vs `/`) may cause issues
- **Solution:** Use forward slashes (`/`) in volume paths in `docker-compose.yml`
  ```yaml
  volumes:
    - ./airflow-local/dags:/opt/airflow/dags  # Use forward slashes
  ```

#### **Issue: "Port already in use" on Windows**
- **Symptom:** Port 8080, 5000, etc. already in use
- **PowerShell Solution:**
  ```powershell
  # Find process using port 8080
  netstat -ano | findstr :8080
  
  # Kill process by PID (replace 12345 with actual PID)
  taskkill /PID 12345 /F
  ```
- **Alternative:** Modify port mappings in `docker-compose.yml`:
  ```yaml
  ports:
    - "8081:8080"  # Use 8081 instead of 8080
  ```

#### **Issue: Docker Memory Issues on Windows**
- **Symptom:** "out of memory" errors, containers crashing
- **Solution:**
  1. Open Docker Desktop → Settings → Resources
  2. Increase Memory slider to 8GB or more
  3. Click "Apply & Restart"

#### **Issue: Volume Mounts Not Working on Windows**
- **Symptom:** DAGs folder appears empty in Airflow
- **Solution:**
  1. Check if file sharing is enabled in Docker Desktop:
     - Settings → Resources → File Sharing
     - Ensure your project directory is listed
  2. Verify volume mount paths use forward slashes
  3. Restart Docker: `docker compose restart`

---

### **General Issues (All Platforms)**

#### **Issue: Airflow DAGs Not Visible**
- **Cause:** DAG files not in the mounted `airflow-local/dags/` folder
- **Fix:**
  1. Ensure `docker-compose.yml` volume mounts `./airflow-local/dags:/opt/airflow/dags`
  2. Check files exist: `ls airflow-local/dags/` (Linux/Mac) or `dir airflow-local\dags\` (Windows)
  3. Restart Airflow scheduler: `docker compose restart airflow-scheduler`
  4. Wait 30-60 seconds for DAGs to appear in Airflow UI

#### **Issue: MLflow Experiments Not Saving**
- **Cause:** MinIO or PostgreSQL connection failure
- **Fix:**
  1. Check MinIO console at `http://localhost:9001` (credentials: minio_user / minio_pwd)
  2. Verify PostgreSQL is running:
     ```bash
     docker compose logs postgres
     ```
  3. Check MLflow logs:
     ```bash
     docker compose logs mlflow
     ```
  4. Verify `config.env` credentials match Docker Compose environment variables

#### **Issue: Grafana Dashboards Empty**
- **Cause:** PostgreSQL data not being written
- **Fix:**
  1. Check `dag_ml_monitoring.py` logs in Airflow UI for errors
  2. Verify drift metrics table exists:
     ```sql
     SELECT * FROM drift_metrics;
     ```
  3. Connect to PostgreSQL:
     ```bash
     docker compose exec postgres psql -U postgres -d airflow
     ```
  4. Check data is being inserted:
     ```sql
     SELECT COUNT(*) FROM drift_metrics;
     ```

#### **Issue: Container Port Conflicts**
If ports are already in use, identify and free them:

**Windows (PowerShell):**
```powershell
# Find which process is using port 8080
netstat -ano | findstr :8080

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Restart Docker containers
docker compose restart
```

**Linux/Mac:**
```bash
# Find which process is using port 8080
lsof -i :8080

# Kill the process
kill -9 <PID>

# Restart Docker containers
docker compose restart
```

**Alternative - Change Port in docker-compose.yml:**
```yaml
services:
  airflow-webserver:
    ports:
      - "8081:8080"  # External port 8081 → Internal port 8080
```
Then restart: `docker compose restart`

#### **Issue: Services Not Responding After Restart**
- **Solution:**
  1. Stop all containers: `docker compose down`
  2. Remove unused resources: `docker system prune -a`
  3. Rebuild and restart:
     ```bash
     docker compose --env-file config.env up -d
     ```
  4. Wait 1-2 minutes for services to fully initialize
  5. Check status: `docker compose ps`

#### **Issue: "Cannot connect to Docker daemon"**
- **Windows:** Ensure Docker Desktop application is running (check system tray)
- **Linux:** Start Docker service: `sudo systemctl start docker`
- **Verify:** Run `docker ps` to confirm connection

#### **Issue: High CPU or Memory Usage**
- **Solution:**
  1. Check container resource usage:
     ```bash
     docker stats
     ```
  2. Identify problematic container
  3. Check logs:
     ```bash
     docker compose logs <service-name> -f
     ```
  4. Consider reducing Airflow workers or parallelism in `config.env`

---

## 💬 Getting Help & Support

### **For Windows Users**

If you encounter issues specific to Windows:

1. **Check WSL 2 Status:**
   ```powershell
   wsl --version
   wsl -l -v
   ```
   Ensure the default distribution uses version 2.

2. **Docker Desktop Diagnostics:**
   - Settings → Resources: Increase memory if needed
   - Settings → File Sharing: Ensure project directory is included
   - Restart Docker Desktop completely if having issues

3. **Clear Docker Cache:**
   ```powershell
   docker system prune -a
   docker builder prune
   ```

4. **Reinstall WSL 2 (if all else fails):**
   ```powershell
   wsl --unregister Ubuntu  # Replace Ubuntu with your distro name
   wsl --install
   ```

### **Common Questions**

**Q: Can I use this on Windows without Docker Desktop?**
A: Not recommended. Docker is required for the orchestrated environment. Docker Desktop with WSL 2 is the simplest approach.

**Q: Can I modify Python code inside containers?**
A: Yes! Edit files in `src/` and `airflow-local/dags/` directly. Changes are mounted and picked up automatically (except Python packages, which need reinstallation).

**Q: How do I access databases from outside Docker?**
A: Services are exposed on localhost:
- PostgreSQL: `localhost:5432` (user: `postgres`, password: `postgres`)
- MinIO: `localhost:9000` (S3 API), `localhost:9001` (web console)
- Use standard tools like pgAdmin, DBeaver, or aws-cli

**Q: Can I run this on multiple computers?**
A: Yes, but change `localhost` to your machine's IP address and update Docker Compose ports accordingly.

**Q: My DAGs aren't showing up in Airflow. What's wrong?**
A: 
1. Verify files exist in `airflow-local/dags/` 
2. Check Docker volume mount: `docker compose exec airflow-webserver ls -la /opt/airflow/dags/`
3. Check Airflow logs: `docker compose logs airflow-scheduler`
4. Wait 60+ seconds after starting for DAGs to appear

**Q: How do I reset everything to a fresh start?**
A: 
```powershell
docker compose down -v
docker system prune -a
docker compose --env-file config.env up -d
```
⚠️ This deletes all data, experiments, and models!

### **Resources for Learning**

- **Apache Airflow:** https://airflow.apache.org/docs/
- **MLflow:** https://mlflow.org/docs/
- **Docker:** https://docs.docker.com/
- **PostgreSQL:** https://www.postgresql.org/docs/
- **Grafana:** https://grafana.com/grafana/dashboards/

### **Reporting Issues**

If you find a bug:

1. **Check existing issues** on GitHub
2. **Gather diagnostic info:**
   ```powershell
   docker compose ps
   docker compose logs > logs.txt
   docker --version
   wsl --version
   ```
3. **Create a GitHub issue** with:
   - Error message/screenshots
   - Steps to reproduce
   - Your environment (Windows version, Docker version, etc.)
   - Diagnostic output from above

### **Contact**

- **Project Repository:** https://github.com/oktavianidewi/mlops-zc-2025
- **MLOps Zoomcamp:** https://github.com/DataTalksClub/mlops-zoomcamp

---

## 📚 Data Dictionary

### Input Features (Diabetes Dataset)
| Feature | Type | Description |
|---------|------|-------------|
| Pregnancies | Int | Number of pregnancies |
| Glucose | Float | Plasma glucose concentration |
| BloodPressure | Float | Diastolic blood pressure (mm Hg) |
| SkinThickness | Float | Triceps skin fold thickness (mm) |
| Insulin | Float | 2-Hour serum insulin (mu U/ml) |
| BMI | Float | Body mass index |
| DiabetesPedigreeFunction | Float | Genetic risk indicator |
| Age | Int | Age in years |
| Outcome | Int | Target: 1 = diabetes, 0 = no diabetes |

### PostgreSQL Tables

**drift_metrics**
- `id`: Auto-increment primary key
- `drift_score`: Numerical drift detection score (0-1)
- `metrics_json`: Full JSON payload of all metrics
- `timestamp`: When the drift was detected
- `model_version`: Which model version was used

**model_metadata**
- `id`: Auto-increment primary key
- `model_name`: e.g., "diabetes_predictor"
- `version`: Version number
- `accuracy`: Model accuracy on test set
- `timestamp`: Training time
- `minio_path`: S3 path to model binary

---

## 🚀 Next Steps & Improvements

### Enhancements for Production
- [ ] Add unit tests for pipeline steps
- [ ] Implement CI/CD pipeline (GitHub Actions/GitLab CI)
- [ ] Add authentication to all web services
- [ ] Switch to `CeleryExecutor` for scalable Airflow
- [ ] Implement model versioning with proper rollback strategy
- [ ] Add data quality checks (Great Expectations)
- [ ] Set up centralized logging (ELK stack or Datadog)
- [ ] Add alerts for drift exceeding thresholds (PagerDuty/Slack)

### Feature Ideas
- [ ] Support multiple model types (Random Forest, XGBoost, Neural Networks)
- [ ] Add hyperparameter tuning (Optuna/Ray Tune)
- [ ] Implement A/B testing for model comparison
- [ ] Add explainability features (SHAP values in prediction output)
- [ ] Create custom Grafana alerts for automated actions
- [ ] Support incremental retraining vs. full retraining

---

## 📖 Resources

- [Airflow Documentation](https://airflow.apache.org/docs/)
- [MLflow Documentation](https://mlflow.org/docs/)
- [Evidently AI Drift Detection](https://docs.evidentlyai.com/)
- [Grafana Dashboard Guide](https://grafana.com/grafana/dashboards/)
- [Pima Indians Diabetes Dataset](https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database)

---

## 📝 License

This project is created for educational purposes as part of the MLOps Zoomcamp.