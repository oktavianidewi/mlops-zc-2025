import os
import kagglehub


def ingestion_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.environ["KAGGLEHUB_CACHE"] = f"{current_dir}/data"

    # Download latest version
    location = kagglehub.dataset_download("uciml/pima-indians-diabetes-database", force_download=True)

    print("Path to dataset files:", location)

ingestion_data()