from kaggle.api.kaggle_api_extended import KaggleApi
import os

# Function to download dataset from Kaggle
def download_kaggle_dataset():
    api = KaggleApi()
    api.authenticate()
    download_path = 'data/controlDataset1'
    api.dataset_download_files('debashish311601/formula-1-official-data-19502022', path='data/controlDataset1', unzip=True)
    print(f"Dataset downloaded to: {os.path.abspath(download_path)}")
    
if __name__ == "__main__":
    download_kaggle_dataset()