import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import os 
import random
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.dir import df_save_to_csv

# Play around with the drift_amount to control how drifted are the data
def introduce_drift(data, drift_features, drift_amount=0.1, random_seed=42):
    np.random.seed(random_seed)
    drifted_data = data.copy()
    
    for feature in drift_features:
        if feature in data.columns:
            drifted_data[feature] += np.random.normal(loc=0, scale=drift_amount, size=data.shape[0])
    
    return drifted_data
    
# parent_path = 'pipeline/data' # local
parent_path = '/opt/airflow/src/pipeline/data' # docker

# read data
data_path = f'{parent_path}/datasets/uciml/pima-indians-diabetes-database/versions/1/diabetes.csv'

df = pd.read_csv(data_path)

# split X/y
X = df.drop('Outcome', axis=1)
y = df['Outcome']

features_to_drift = ['Glucose', 'BloodPressure', 'SkinThickness', 'Pregnancies']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

random_amount = random.randint(50, 200)
drifted_data = introduce_drift(X_test, features_to_drift, drift_amount=random_amount)
drifted_data = drifted_data.reset_index(drop = True)

# reference_data['Outcome'] = y_train.reset_index(drop = True)
drifted_data['Outcome'] = y_test.reset_index(drop = True)

df_save_to_csv(drifted_data, 'data', 'new_data.csv')
print(f"drift data created with random amount of {random_amount}.")

