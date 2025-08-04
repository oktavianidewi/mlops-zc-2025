import os

def create_folder_file(folder_name, file_name):
    file_path = f"{folder_name}/{file_name}"
    if not os.path.exists(file_path):
        os.makedirs(folder_name, exist_ok=True)
        open(file_path, "w").close()

def df_save_to_csv(df, folder_name, file_name):
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    path = f"{parent_dir}/pipeline/{folder_name}/{file_name}"
    df.to_csv(f'{path}', index=False)
