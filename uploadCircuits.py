import pandas as pd
from sqlalchemy import create_engine



# Function to transform and load data in chunks
def transform_and_load_to_db():
	# Database connection details
	db_user = 'airflow'
	db_password = 'airflow'
	db_host = 'localhost'
	db_port = '5432'
	db_name = 'postgres'

	# Create SQLAlchemy engine
	engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
	print("Engine has been created")

	file_path = 'data/circuits.csv'

	# Read and process data in chunks
	chunk_size = 10000
	for chunk in pd.read_csv(file_path, chunksize=chunk_size):
		processed_rows = []
		# print(chunk.iloc[0])
		# Load data into database

		for index, row in chunk.iterrows():
			# Perform your checks on each row
			# Example check: ensure no missing values in critical columns
			if pd.notnull(row['circuitId']) and pd.notnull(row['name']):
				try:
					row['alt'] = int(row['alt'])
				except ValueError:
					row['alt'] = 0
				try:
					row['lat'] = int(row['lat'])
				except ValueError:
					row['lat'] = 0
				try:
					row['lng'] = int(row['lng'])
				except ValueError:
					row['lng'] = 0
				# You can also perform transformations here if needed
				processed_rows.append(row)

		# Convert the list of processed rows to a DataFrame
		processed_df = pd.DataFrame(processed_rows)

		if not processed_df.empty:
			# Load the processed DataFrame into the database
			processed_df.to_sql('dim_circuits', engine, if_exists='append', index=False)

		print(f"Processed and uploaded a chunk of {len(processed_df)} rows")

if __name__ == "__main__":    
	# Transform and load data into PostgreSQL
	transform_and_load_to_db()
