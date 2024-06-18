from kaggle.api.kaggle_api_extended import KaggleApi
import os

# Function to download dataset from Kaggle
def download_kaggle_dataset():
    api = KaggleApi()
    api.authenticate()
    download_path = 'data/controlDataset2'
    api.dataset_download_files('rprkh15/f1-race-and-qualifying-data', path='data/controlDataset2', unzip=True)
    print(f"Dataset downloaded to: {os.path.abspath(download_path)}")
    
if __name__ == "__main__":
    download_kaggle_dataset()