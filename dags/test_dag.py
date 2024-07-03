import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'simple_test_dag',
    default_args=default_args,
    description='A simple test DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

# Path to the scripts directory
scripts_dir = os.path.join(os.path.dirname(__file__), 'scripts')


t1 = DummyOperator(
    task_id='dummy_task',
    dag=dag,
)

t2 = BashOperator(
    task_id='conn_test',
    bash_command=f'python {os.path.join(scripts_dir, "connectionTest.py")}',
    dag=dag,
)

t1 >> t2