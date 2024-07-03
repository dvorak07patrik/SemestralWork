import os
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime, timedelta

def check_data(**kwargs):
    # Replace with the actual path where the data should be downloaded
    data_dir = os.path.join(os.path.dirname(__file__), 'scripts/data')
    print(data_dir)
    if not os.path.exists(data_dir) or not os.listdir(data_dir):
        raise ValueError('No data downloaded')

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'f1_etl_workflow',
    default_args=default_args,
    description='ETL workflow for Formula 1 data',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,  # Do not schedule periodically
    catchup=False, 
    max_active_runs=1,
)

# Path to the scripts directory
scripts_dir = os.path.join(os.path.dirname(__file__), 'scripts')

t1 = BashOperator(
    task_id='create_database',
    bash_command=f'python {os.path.join(scripts_dir, "databaseCreation.py")}',
    dag=dag,
)

t2 = BashOperator(
    task_id='download_first_dataset',
    bash_command=f'python {os.path.join(scripts_dir, "downloadFirstDataset.py")}',
    dag=dag,
)

t2_check = PythonOperator(
    task_id='check_downloaded_data',
    python_callable=check_data,
    provide_context=True,
    dag=dag,
)

no_data = DummyOperator(
    task_id='no_data',
    dag=dag,
)

t3 = BashOperator(
    task_id='upload_circuits',
    bash_command=f'python {os.path.join(scripts_dir, "uploadCircuits.py")}',
    dag=dag,
)

t4 = BashOperator(
    task_id='upload_constructors',
    bash_command=f'python {os.path.join(scripts_dir, "uploadConstructors.py")}',
    dag=dag,
)

t5 = BashOperator(
    task_id='upload_drivers',
    bash_command=f'python {os.path.join(scripts_dir, "uploadDrivers.py")}',
    dag=dag,
)

t6 = BashOperator(
    task_id='upload_races',
    bash_command=f'python {os.path.join(scripts_dir, "uploadRaces.py")}',
    dag=dag,
)

t7 = BashOperator(
    task_id='upload_results',
    bash_command=f'python {os.path.join(scripts_dir, "uploadResults.py")}',
    dag=dag,
)

t8 = BashOperator(
    task_id='upload_constructor_standings',
    bash_command=f'python {os.path.join(scripts_dir, "uploadConstructorStandings.py")}',
    dag=dag,
)

t9 = BashOperator(
    task_id='upload_driver_standings',
    bash_command=f'python {os.path.join(scripts_dir, "uploadDriverStandings.py")}',
    dag=dag,
)

t10 = BashOperator(
    task_id='upload_pit_stops',
    bash_command=f'python {os.path.join(scripts_dir, "uploadPitStops.py")}',
    dag=dag,
)

t11 = BashOperator(
    task_id='upload_qualifying',
    bash_command=f'python {os.path.join(scripts_dir, "uploadQualifying.py")}',
    dag=dag,
)

t12 = BashOperator(
    task_id='upload_lap_times',
    bash_command=f'python {os.path.join(scripts_dir, "uploadLapTimes.py")}',
    dag=dag,
)

t13 = BashOperator(
    task_id='download_race_events_dataset',
    bash_command=f'python {os.path.join(scripts_dir, "downloadRaceEventsDataset.py")}',
    dag=dag,
)

t13_check = PythonOperator(
    task_id='check_downloaded_race_events_data',
    python_callable=check_data,
    provide_context=True,
    dag=dag,
)

t14 = BashOperator(
    task_id='upload_safety_cars',
    bash_command=f'python {os.path.join(scripts_dir, "uploadSafetyCars.py")}',
    dag=dag,
)

t15 = BashOperator(
    task_id='upload_red_flags',
    bash_command=f'python {os.path.join(scripts_dir, "uploadRedFlags.py")}',
    dag=dag,
)

end = DummyOperator(
    task_id='end',
    trigger_rule=TriggerRule.ALL_DONE,  # Proceed to this task regardless of previous task status
    dag=dag,
)


# Setting up the dependencies
t1 >> t2 >> t2_check
t2_check >> [t3, no_data]
t3 >> t4 >> t5 >> t6 >> t7 >> t8 >> t9 >> t10 >> t11 >> t12 >> t13 >> t13_check
t13_check >> [t14, no_data]
t14 >> t15 >> end
no_data >> end
