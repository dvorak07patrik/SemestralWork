import psycopg2

try:
    # Establish connection to PostgreSQL
    connection = psycopg2.connect(
        user="airflow",
        password="airflow",
        host="postgres",
        port="5432",
        database="postgres"
    )

    cursor = connection.cursor()
    # Execute a test query
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print(f"You are connected to - {record}\n")

    # Close the cursor and connection
    cursor.close()
    connection.close()
except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
