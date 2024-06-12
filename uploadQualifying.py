import os
import pandas as pd
from sqlalchemy import create_engine, text
	
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
	

	file_path = 'data/qualifying.csv'

	# Read and process data in chunks
	chunk_size = 10000
	for chunk in pd.read_csv(file_path, chunksize=chunk_size):
		processed_rows = []
		# print(chunk.iloc[0])
		# Load data into database

		for index, row in chunk.iterrows():
			# Perform your checks on each row
			# Example check: ensure no missing values in critical columns
			if pd.notnull(row['qualifyId']) and race_exists(row['raceId']) and driver_exists(row['driverId']) and constructor_exists(row['constructorId']):
				# Validate and possibly replace date and time fields
				try:
					row['number'] = int(row['number'])
				except ValueError:
					row['number'] = 0
				
				try:
					row['position'] = int(row['position'])
				except ValueError:
					row['position'] = 0
				
				processed_rows.append(row)

		# Convert the list of processed rows to a DataFrame
		processed_df = pd.DataFrame(processed_rows)

		if not processed_df.empty:
			# Load the processed DataFrame into the database
			processed_df.to_sql('fact_qualifying', engine, if_exists='append', index=False)

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
	# Step 2: Transform and load data into PostgreSQL
	transform_and_load_to_db()
