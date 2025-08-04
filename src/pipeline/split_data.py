import pandas as pd
from sklearn.model_selection import train_test_split

parent_path = '/opt/airflow/src/pipeline/data'

def split_data():
    # read data
    data_path = f'{parent_path}/datasets/uciml/pima-indians-diabetes-database/versions/1/diabetes.csv'
    df = pd.read_csv(data_path)

    # split X/y
    X = df.drop('Outcome', axis=1)
    y = df['Outcome']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=100)
    
    # store to X_train.csv, X_test.csv, y_train.csv, y_test.csv

    map_path_df = {
        'X': {
            'path': f'{parent_path}/X.csv',
            'df': X
        },
        'X_train': {
            'path': f'{parent_path}/X_train.csv',
            'df': X_train
        },
        'X_test': {
            'path': f'{parent_path}/X_test.csv',
            'df': X_test
        },
        'y_train': {
            'path': f'{parent_path}/y_train.csv',
            'df': y_train
        },
        'y_test': {
            'path': f'{parent_path}/y_test.csv',
            'df': y_test
        }
    }

    for key, value in map_path_df.items():
        path = value['path']
        df = value['df']
        try:
            df.to_csv(path, index=False)
            print(f"File saved successfully to: {path}.")
        except Exception as e:
            print(f"Error saving file: {e}")

split_data()