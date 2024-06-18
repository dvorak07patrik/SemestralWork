import os
import pandas as pd
from sqlalchemy import create_engine, text
from kaggle.api.kaggle_api_extended import KaggleApi
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

# Database connection details
db_user = 'postgres'
db_password = 'mysecretpassword'
db_host = 'localhost'
db_port = '5432'
db_name = 'postgres'

# Create SQLAlchemy engine
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# Function to download dataset from Kaggle
def download_kaggle_dataset(**kwargs):
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files('rohanrao/formula-1-world-championship-1950-2020', path='/tmp/data', unzip=True)

# Function to check if new data is available on Kaggle
def is_new_data_available(**kwargs):
    api = KaggleApi()
    api.authenticate()
    dataset_metadata = api.dataset_view('rohanrao/formula-1-world-championship-1950-2020')
    last_update_time = dataset_metadata.lastUpdated.isoformat()
    
    ti = kwargs['ti']
    ti.xcom_push(key='last_update_time', value=last_update_time)
    
    last_download_time = get_last_update_time()
    if last_update_time > last_download_time:
        return 'download_data'
    return 'no_new_data'

# Function to get the last update time of the dataset
def get_last_update_time():
    try:
        with open('/tmp/last_download_time.txt', 'r') as file:
            last_download_time = file.readline().strip()
    except FileNotFoundError:
        last_download_time = '1970-01-01T00:00:00Z'
    return last_download_time

# Function to set the last update time of the dataset
def set_last_update_time(**kwargs):
    ti = kwargs['ti']
    last_update_time = ti.xcom_pull(key='last_update_time', task_ids='check_for_new_data')
    with open('/tmp/last_download_time.txt', 'w') as file:
        file.write(last_update_time)

# Function to transform and load data into the database
def transform_and_load_to_db():
    file_path = '/tmp/data/safety_cars.csv'
    chunk_size = 10000
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        processed_rows = []
        for index, row in chunk.iterrows():
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

# Function to check if an entry already exists in the database
def entry_exists(table_name, row):
    with engine.connect() as connection:
        query = text(f'SELECT 1 FROM {table_name} WHERE "raceId" = :raceId AND "cause" = :cause AND "deployed" = :deployed AND "retreated" = :retreated AND "fullLaps" = :fullLaps')
        result = connection.execute(query, row).fetchone()
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
    'start_date': datetime(2023, 1, 1),
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
    schedule_interval='@daily',
)

# Define the tasks
check_for_new_data = PythonOperator(
    task_id='check_for_new_data',
    python_callable=is_new_data_available,
    provide_context=True,
    dag=dag,
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

update_last_download_time = PythonOperator(
    task_id='update_last_download_time',
    python_callable=set_last_update_time,
    provide_context=True,
    dag=dag,
)

no_new_data = DummyOperator(
    task_id='no_new_data',
    dag=dag,
)

# Define the task dependencies
check_for_new_data >> [download_data, no_new_data]
download_data >> transform_and_load_data >> update_last_download_time
