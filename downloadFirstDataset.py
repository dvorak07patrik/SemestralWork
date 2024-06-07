from kaggle.api.kaggle_api_extended import KaggleApi
import os

# Function to download dataset from Kaggle
def download_kaggle_dataset():
    api = KaggleApi()
    api.authenticate()
    download_path = 'data'
    api.dataset_download_files('rohanrao/formula-1-world-championship-1950-2020', path='data', unzip=True)
    print(f"Dataset downloaded to: {os.path.abspath(download_path)}")
    
if __name__ == "__main__":
    download_kaggle_dataset()