import os
import pandas as pd
from sqlalchemy import create_engine, text
import datetime



def compare_positions(original, first, second):
	if original == 0:
		original == "NC"
	if first == second and first != original:
		if first == "NC":
			first = 0
		return first
	return None


def compare_points(original, first, second):
	if first == second and first != original:
		return first
	return None

def find_driver(name):
	first_name = name[0]
	last_name = name[1]
	with engine.connect() as connection:
		for i in range(2, len(name)):
			last_name += " " + name[i]
		query = text(f'SELECT driverId FROM dim_drivers WHERE "forename" = {first_name} AND "surname" = {last_name}')
		result = connection.execute(query).scalar()
	return result


def find_race(year, race_name):
	with engine.connect() as connection:
		if (race_name[:4] != "Aust"):
			query = text(f'SELECT raceId FROM dim_races WHERE "season" = {year} AND "name" LIKE "%" || {race_name[:4]} || "%"')
		else:
			if (race_name == "Australia"):
				query = text(f'SELECT raceId FROM dim_races WHERE "season" = {year} AND "name" LIKE "%Australian%"')
			else:
				query = text(f'SELECT raceId FROM dim_races WHERE "season" = {year} AND "name" LIKE "%Austrian%"')
		result = connection.execute(query).scalar()
	return result

# Function to transform and load data in chunks
def transform_and_load_to_db():
	file_path = 'data/controlDataset1/race_details.csv'
	table_name_base = '_race_results.csv'
	separator = '-'
	# Read and process data in chunks
	chunk_size = 10000
	for chunk in pd.read_csv(file_path, chunksize=chunk_size):
		for index, row in chunk.iterrows():
			grand_prix_name = str(row['Grand Prix']).split()
			sec_dataset_table_name = separator.join(grand_prix_name) + table_name_base
			second_dataset_race_path = f'data/controlDataset2/{row['Year']}/Race Results/' + sec_dataset_table_name

			table = pd.read_csv(second_dataset_race_path)
			for sec_table_row in table.iterrows():
				if row['Driver'] == sec_table_row['Driver']:
					race_id = find_race(row['Year'], row['Grand Prix'])
					driver_id = find_driver(str(row['Driver']).split())
					if race_id is not None and driver_id is not None:
						with engine.connect() as connection:
							query = text(f'SELECT * FROM fact_results WHERE "raceId" = {race_id} AND "driverId" = {driver_id}')
							original_row = connection.execute(query).fetchone()
						new_position = compare_positions(original_row['position'], row['Pos'], sec_table_row['Position'])
						if new_position is not None:
							with engine.connect() as connection:
								query = text(f'UPDATE fact_results SET position = {new_position} WHERE "resultId" = {original_row['resultId']}')
								connection.execute(query)
								query = text(f'UPDATE fact_results SET positionText = {new_position} WHERE "resultId" = {original_row['resultId']}')
								connection.execute(query)
								query = text(f'UPDATE fact_results SET positionOrder = {new_position} WHERE "resultId" = {original_row['resultId']}')
								connection.execute(query)
						new_points = compare_points(original_row['points'], row['PTS'], sec_table_row['Points'])
						if new_points is not None:
							with engine.connect() as connection:
								query = text(f'UPDATE fact_results SET points = {new_points} WHERE "resultId" = {original_row['resultId']}')
								connection.execute(query)

							


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
