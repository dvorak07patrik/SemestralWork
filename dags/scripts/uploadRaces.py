import os
import pandas as pd
from sqlalchemy import create_engine, text
import datetime

# Function to check if a value is a valid date
def is_valid_date(date_str):
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Function to check if a value is a valid time
def is_valid_time(time_str):
    try:
        datetime.datetime.strptime(time_str, '%H:%M:%S')
        return True
    except ValueError:
        return False
	
# Function to check if circuitId exists in dim_circuits table
def circuit_exists(circuit_id):
	with engine.connect() as connection:
		query = text(f'SELECT EXISTS(SELECT 1 FROM dim_circuits WHERE "circuitId" = {circuit_id})')
		result = connection.execute(query).scalar()
	return result

# Function to transform and load data in chunks
def transform_and_load_to_db():
	

	file_path = os.path.join(os.path.dirname(__file__), 'data/races.csv')

	# Define default values for invalid date and time
	default_date = '0000-00-00'
	default_time = '00:00:00'
	# Read and process data in chunks
	chunk_size = 10000
	for chunk in pd.read_csv(file_path, chunksize=chunk_size):
		chunk.rename(columns={
        'year': 'season',
        
    }, inplace=True)
		processed_rows = []
		# print(chunk.iloc[0])
		# Load data into database

		for index, row in chunk.iterrows():
			# Perform your checks on each row
			# Example check: ensure no missing values in critical columns
			if pd.notnull(row['raceId']) and pd.notnull(row['name']) and circuit_exists(row['circuitId']):
				# Validate and possibly replace date and time fields
				row['date'] = row['date'] if is_valid_date(row['date']) else default_date
				row['time'] = row['time'] if is_valid_time(row['time']) else default_time
				

				"""
				row['fp1_date'] = row['fp1_date'] if is_valid_date(row['fp1_date']) else default_date
				row['fp1_time'] = row['fp1_time'] if is_valid_time(row['fp1_time']) else default_time
				row['fp2_date'] = row['fp2_date'] if is_valid_date(row['fp2_date']) else default_date
				row['fp2_time'] = row['fp2_time'] if is_valid_time(row['fp2_time']) else default_time
				row['fp3_date'] = row['fp3_date'] if is_valid_date(row['fp3_date']) else default_date
				row['fp3_time'] = row['fp3_time'] if is_valid_time(row['fp3_time']) else default_time
				row['quali_date'] = row['quali_date'] if is_valid_date(row['quali_date']) else default_date
				row['quali_time'] = row['quali_time'] if is_valid_time(row['quali_time']) else default_time
				row['sprint_date'] = row['sprint_date'] if is_valid_date(row['sprint_date']) else default_date
				row['sprint_time'] = row['sprint_time'] if is_valid_time(row['sprint_time']) else default_time
				"""

				try:
					row['season'] = int(row['season'])
				except ValueError:
					row['season'] = 0
				
				try:
					row['round'] = int(row['round'])
				except ValueError:
					row['round'] = 0

				processed_rows.append(row)

		# Columns to exclude
		columns_to_exclude = ['fp1_date', 'fp1_time', 'fp2_date', 'fp2_time', 'fp3_date', 'fp3_time', 'quali_date', 'quali_time', 'sprint_date', 'sprint_time']

		# Convert the list of processed rows to a DataFrame
		processed_df = pd.DataFrame(processed_rows)
		# Drop the columns I want to exclude
		processed_df = processed_df.drop(columns=columns_to_exclude)

		if not processed_df.empty:
			# Load the processed DataFrame into the database
			processed_df.to_sql('dim_races', engine, if_exists='append', index=False)

		print(f"Processed and uploaded a chunk of {len(processed_df)} rows")

if __name__ == "__main__":    
	# Database connection details
	db_user = 'airflow'
	db_password = 'airflow'
	db_host = 'postgres'
	db_port = '5432'
	db_name = 'postgres'

	# Create SQLAlchemy engine
	engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
	print("Engine has been created")
	# Transform and load data into PostgreSQL
	transform_and_load_to_db()
