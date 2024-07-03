import os
import pandas as pd
from sqlalchemy import create_engine, text

def find_race_id(season, name):
	with engine.connect() as connection:
		query = text('SELECT "raceId" FROM dim_races WHERE "season" = :season AND "name" = :name')
		result = connection.execute(query, {"season": season, "name": name}).fetchone()
		#print(result[0])
		if result:
			return result[0]
		else:
			print(f"{season} {name}")


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

# Function to transform and load data in chunks
def transform_and_load_to_db():
	

	file_path = os.path.join(os.path.dirname(__file__), 'data/red_flags.csv')

	# Read and process data in chunks
	chunk_size = 10000
	for chunk in pd.read_csv(file_path, chunksize=chunk_size, dtype={'Excluded': str}):
		chunk['Excluded'] = chunk['Excluded'].astype(str)
		processed_rows = []
		# Load data into database
		new_row = {"raceId": 0, "lap": 0, "resumed": 0, "incident": "", "excluded": ""}
		new_row = pd.Series(new_row)
		
		for index, row in chunk.iterrows():
			#print(type(row))
			# Perform checks on each row
			race_name, season = extract_season_and_race(row['Race'])
			raceId = find_race_id(season, race_name)
			if raceId is not None:
				new_row['raceId'] = raceId
				new_row['incident'] = row['Incident']
				if len(new_row['incident']) > 255:
					new_row['incident'] = new_row['incident'][0:255] # can be change later
				new_row['excluded'] = row['Excluded']
				if len(new_row['excluded']) > 255:
					new_row['excluded'] = new_row['excluded'][0:255] # can be change later
				
				try:
					new_row['lap'] = int(row['Lap'])
				except ValueError:
					new_row['lap'] = 0
				
				try:
					new_row['resumed'] = int(row['Resumed'])
				except ValueError:
					new_row['resumed'] = 0
				
				processed_rows.append(new_row)
				new_row = {"raceId": 0, "lap": 0, "resumed": 0, "incident": "", "excluded": ""}
				new_row = pd.Series(new_row)

		# Convert the list of processed rows to a DataFrame
		processed_df = pd.DataFrame(processed_rows)

		if not processed_df.empty:
			# Load the processed DataFrame into the database
			processed_df.to_sql('fact_red_flags', engine, if_exists='append', index=False)

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
	transform_and_load_to_db()
