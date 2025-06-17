import snowflake.connector
import csv
import os
from utils.constants import PROCESSED_PATH,USER,ACCOUNT,PASSWORD,WAREHOUSE,DATABASE,SCHEMA

# Snowflake connection parameters

#SNOWFLAKE_TABLE = 'Movies'
#CSV_FILE_PATH = os.path.join(PROCESSED_PATH,f"merged_movies_with_genre.csv")


def connect_to_snowflake() -> snowflake.connector.connection.SnowflakeConnection:
    try:
        # Establish connection to Snowflake
        conn = snowflake.connector.connect(
            user=USER,
            password=PASSWORD,
            account=ACCOUNT,
            warehouse=WAREHOUSE,
            database=DATABASE,
            schema=SCHEMA
        )
        print("Successfully connected to Snowflake")
        return conn
    except Exception as e:
        print(f"Failed to connect to Snowflake: {str(e)}")
        raise


def upload_to_snowflake(conn: snowflake.connector.connection.SnowflakeConnection):
    SNOWFLAKE_TABLE = 'Movies'
    CSV_FILE_PATH = os.path.join(PROCESSED_PATH, f"merged_movies_with_genre.csv")
    conn = conn
    try:
        # Create a cursor
        cursor = conn.cursor()

        # Check if CSV file exists
        if not os.path.exists(CSV_FILE_PATH):
            raise FileNotFoundError(f"CSV file not found at {CSV_FILE_PATH}")

        # Read CSV and insert rows
        with open(CSV_FILE_PATH, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)  # Skip header row
            for row in csv_reader:
                # Construct INSERT query (assumes columns match CSV order)
                placeholders = ','.join(['%s'] * len(row))
                insert_query = f"""
                INSERT INTO {DATABASE}.{SCHEMA}."{SNOWFLAKE_TABLE}"
                VALUES ({placeholders})
                """
                cursor.execute(insert_query, row)
        conn.commit()
        print(f"Successfully uploaded CSV to {SNOWFLAKE_TABLE}")

    except snowflake.connector.errors.ProgrammingError as e:
        print(f"Snowflake error: {e}")
        conn.rollback()
    except FileNotFoundError as e:
        print(f"File error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
            print("Snowflake connection closed")
'''
if __name__ == "__main__":
    upload_csv_to_snowflake()
'''