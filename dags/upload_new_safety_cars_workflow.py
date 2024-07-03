import os
import pandas as pd
from sqlalchemy import create_engine, text
from kaggle.api.kaggle_api_extended import KaggleApi
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

# Database connection details
db_user = 'airflow'
db_password = 'airflow'
db_host = 'postgres'
db_port = '5432'
db_name = 'postgres'

# Create SQLAlchemy engine
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')


# Function to download dataset from Kaggle
def download_kaggle_dataset(**kwargs):
    api = KaggleApi()
    api.authenticate()
    data_dir = os.path.join(os.path.dirname(__file__), 'scripts/data')
    download_path = data_dir
    api.dataset_download_files('jtrotman/formula-1-race-events', path=download_path, unzip=True)


# Function to transform and load data into the database
def transform_and_load_to_db():
    data_dir = os.path.join(os.path.dirname(__file__), 'scripts/data')
    new_file_path = os.path.join(data_dir, 'safety_cars.csv')
    old_file_path = os.path.join(data_dir, 'safety_cars_old.csv')

    # If the old file doesn't exist, create it by renaming the new file
    if not os.path.exists(old_file_path):
        os.rename(new_file_path, old_file_path)
        print("No previous file found. Current file will be used as the baseline for future comparisons.")
        return

    # Read both old and new CSV files
    new_data = pd.read_csv(new_file_path)
    old_data = pd.read_csv(old_file_path)

    # Find new rows by comparing the new file to the old file
    new_rows = new_data.merge(old_data, on=list(new_data.columns), how='left', indicator=True)
    new_rows = new_rows[new_rows['_merge'] == 'left_only'].drop(columns=['_merge'])

    # Process and load new rows
    if not new_rows.empty:
        processed_rows = []
        for index, row in new_rows.iterrows():
            race_name, season = extract_season_and_race(row['Race'])
            raceId = find_race_id(season, race_name)
            if raceId is not None:
                new_row = pd.Series({
                    'raceId': raceId,
                    'cause': row['Cause'],
                    'type': "S",
                    'deployed': int(row['Deployed']) if pd.notnull(row['Deployed']) else 0,
                    'retreated': int(row['Retreated']) if pd.notnull(row['Retreated']) else 0,
                    'fullLaps': int(row['FullLaps']) if pd.notnull(row['FullLaps']) else 0
                })
                if not entry_exists('fact_safety_cars', new_row):
                    processed_rows.append(new_row)

        if processed_rows:
            processed_df = pd.DataFrame(processed_rows)
            processed_df.to_sql('fact_safety_cars', engine, if_exists='append', index=False)
        print(f"Processed and uploaded a chunk of {len(processed_rows)} rows")

    # Replace the old file with the new file
    os.remove(old_file_path)
    os.rename(new_file_path, old_file_path)

# Function to check if an entry already exists in the database
def entry_exists(table_name, row):
    with engine.connect() as connection:
        query = text(f'SELECT * FROM {table_name} WHERE "raceId" = :raceId AND "cause" = :cause')
        result = connection.execute(query, {"raceId": row['raceId'], "cause": row['cause']}).fetchone()
    return result is not None

# Function to extract season and race name from race input
def extract_season_and_race(race_input):
    race = race_input.split()
    season = race[0]
    race_name = race[1:]
    race_name_string = ' '.join(map(str, race_name))
    try:
        season_int = int(season)
    except ValueError:
        season_int = 0
    return (race_name_string, season_int)

# Function to find raceId by season and name
def find_race_id(season, name):
    with engine.connect() as connection:
        query = text('SELECT "raceId" FROM dim_races WHERE "season" = :season AND "name" = :name')
        result = connection.execute(query, {"season": season, "name": name}).fetchone()
        return result['raceId'] if result else None

# Define default_args for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 18),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'kaggle_data_workflow',
    default_args=default_args,
    description='A simple workflow to check for new Kaggle data and update the database',
    schedule_interval='@weekly', 
)

download_data = PythonOperator(
    task_id='download_data',
    python_callable=download_kaggle_dataset,
    dag=dag,
)

transform_and_load_data = PythonOperator(
    task_id='transform_and_load_data',
    python_callable=transform_and_load_to_db,
    dag=dag,
)

# Define the task dependencies
download_data >> transform_and_load_data 
