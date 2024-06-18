FROM apache/airflow:2.3.0

USER airflow

# Install kaggle package
RUN pip install kaggle
