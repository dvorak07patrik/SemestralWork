import os
import pandas as pd
from sqlalchemy import create_engine



# Function to transform and load data in chunks
def transform_and_load_to_db():
	# Database connection details
	db_user = 'postgres'
	db_password = 'mysecretpassword'
	db_host = 'localhost'
	db_port = '5432'
	db_name = 'postgres'

	# Create SQLAlchemy engine
	engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
	print("Engine has been created")

	file_path = 'data/drivers.csv'

	# Read and process data in chunks
	chunk_size = 10000
	for chunk in pd.read_csv(file_path, chunksize=chunk_size):
		processed_rows = []
		# print(chunk.iloc[0])
		# Load data into database

		for index, row in chunk.iterrows():
			# Perform your checks on each row
			# Example check: ensure no missing values in critical columns
			if pd.notnull(row['driverId']) and pd.notnull(row['surname']):
				try:
					row['number'] = int(row['number'])
				except ValueError:
					row['number'] = 0

				processed_rows.append(row)

		# Convert the list of processed rows to a DataFrame
		processed_df = pd.DataFrame(processed_rows)

		if not processed_df.empty:
			# Load the processed DataFrame into the database
			processed_df.to_sql('dim_drivers', engine, if_exists='append', index=False)

		print(f"Processed and uploaded a chunk of {len(processed_df)} rows")

if __name__ == "__main__":    
	# Transform and load data into PostgreSQL
	transform_and_load_to_db()
