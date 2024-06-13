import os
import pandas as pd
from sqlalchemy import create_engine, text
import datetime



# Function to check if a value is a valid time
def is_valid_time(time_str):
    try:
        datetime.datetime.strptime(time_str, '%H:%M:%S')
        return True
    except ValueError:
        return False
	
# Function to check if raceId exists in dim_races table
def race_exists(race_id):
	with engine.connect() as connection:
		query = text(f'SELECT EXISTS(SELECT 1 FROM dim_races WHERE "raceId" = {race_id})')
		result = connection.execute(query).scalar()
	return result

def driver_exists(driver_id):
	with engine.connect() as connection:
		query = text(f'SELECT EXISTS(SELECT 1 FROM dim_drivers WHERE "driverId" = {driver_id})')
		result = connection.execute(query).scalar()
	return result

def constructor_exists(constructor_id):
	with engine.connect() as connection:
		query = text(f'SELECT EXISTS(SELECT 1 FROM dim_constructors WHERE "constructorId" = {constructor_id})')
		result = connection.execute(query).scalar()
	return result

# Function to transform and load data in chunks
def transform_and_load_to_db():
	

	file_path = 'data/results.csv'

	# Define default values for invalid date and time
	default_date = '0000-00-00'
	default_time = '00:00:00'
	# Read and process data in chunks
	chunk_size = 10000
	for chunk in pd.read_csv(file_path, chunksize=chunk_size):
		chunk.rename(columns={
        'time': 'timeOrRetired',       
    }, inplace=True)
		processed_rows = []
		# print(chunk.iloc[0])
		# Load data into database

		for index, row in chunk.iterrows():
			# Perform your checks on each row
			# Example check: ensure no missing values in critical columns
			if pd.notnull(row['resultId']) and race_exists(row['raceId']) and driver_exists(row['driverId']) and constructor_exists(row['constructorId']):
				# Validate and possibly replace date and time fields
				try:
					row['number'] = int(row['number'])
				except ValueError:
					row['number'] = 0
				
				try:
					row['grid'] = int(row['grid'])
				except ValueError:
					row['grid'] = 0

				try:
					row['position'] = int(row['position'])
				except ValueError:
					row['position'] = 0
				
				try:
					row['positionOrder'] = int(row['positionOrder'])
				except ValueError:
					row['positionOrder'] = 0

				try:
					row['points'] = int(row['points'])
				except ValueError:
					row['points'] = 0
				processed_rows.append(row)

		# Columns to exclude
		columns_to_exclude = ['laps', 'milliseconds', 'fastestLap', 'rank', 'fastestLapTime', 'fastestLapSpeed', 'statusId']

		# Convert the list of processed rows to a DataFrame
		processed_df = pd.DataFrame(processed_rows)
		# Drop the columns I want to exclude
		processed_df = processed_df.drop(columns=columns_to_exclude)

		if not processed_df.empty:
			# Load the processed DataFrame into the database
			processed_df.to_sql('fact_results', engine, if_exists='append', index=False)

		print(f"Processed and uploaded a chunk of {len(processed_df)} rows")

if __name__ == "__main__":    
	# Database connection details
	db_user = 'postgres'
	db_password = 'mysecretpassword'
	db_host = 'localhost'
	db_port = '5432'
	db_name = 'postgres'

	# Create SQLAlchemy engine
	engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
	print("Engine has been created")
	
	transform_and_load_to_db()
