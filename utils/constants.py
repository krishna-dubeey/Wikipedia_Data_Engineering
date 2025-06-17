import configparser
import os

parser = configparser.ConfigParser()
parser.read(os.path.join(os.path.dirname(__file__), '../config/config.conf'))

SECRET = parser.get('api_keys', 'wikipedia_secret_key')
CLIENT_ID = parser.get('api_keys', 'wikipedia_client_id')
#SUBJECT=parser.get('api_keys','subject')
URL=parser.get('api_keys','url')
#PARAMS=parser.get('api_keys','params')
try:
    START_YEAR=int(parser.get('year','start_year'))
    END_YEAR=int(parser.get('year','end_year'))
except ValueError:
    raise ValueError("START_YEAR and END_YEAR must be integers")

DATABASE_HOST =  parser.get('database', 'database_host')
DATABASE_NAME =  parser.get('database', 'database_name')
DATABASE_PORT =  parser.get('database', 'database_port')
DATABASE_USER =  parser.get('database', 'database_username')
DATABASE_PASSWORD =  parser.get('database', 'database_password')

#AWS
AWS_ACCESS_KEY_ID = parser.get('aws', 'aws_access_key_id')
AWS_ACCESS_KEY = parser.get('aws', 'aws_secret_access_key')
AWS_REGION = parser.get('aws', 'aws_region')
AWS_BUCKET_NAME = parser.get('aws', 'aws_bucket_name')

INPUT_PATH = parser.get('file_paths', 'input_path')
OUTPUT_PATH = parser.get('file_paths', 'output_path')
PROCESSED_PATH=parser.get('file_paths','processed_path')
TABLE_FIELDS = (
    'Title',
    'Cast',
    'Director',
    'Gener',
    'Year'
)

#SNOWFLAKE
ACCOUNT=parser.get('snowflake','account')
USER=parser.get('snowflake','user')
PASSWORD=parser.get('snowflake','password')
ROLE=parser.get('snowflake','role')
WAREHOUSE=parser.get('snowflake','warehouse')
DATABASE=parser.get('snowflake','database')
SCHEMA=parser.get('snowflake','schema')
