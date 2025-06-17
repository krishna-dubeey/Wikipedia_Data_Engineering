import os
import sys
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import subprocess

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pipelines.wikipedia_pipeline import wikipedia_pipeline,wikipedia_pipeline2,wikipedia_pipeline3
from pipelines.snowflake_pipeline import snowflake_pipeline
#generate_year_dates = lambda start, end: [date(year, 1, 1) for year in range(start, end + 1)]

'''
def run_ktr():
    pan_path = "/opt/data-integration/pan.sh"
    ktr_path = "/opt/airflow/transformation/Transformation1Movies.ktr"
    subprocess.run([pan_path, f"/file:{ktr_path}"], check=True)
'''


def run_ktr():
    pan_path = "/opt/data-integration/pan.sh"
    ktr_path = "/opt/transformation/Transformation1Movies.ktr"

    result = subprocess.run(
        [pan_path, f"/file:{ktr_path}"],
        capture_output=True,
        text=True
    )

    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)

    result.check_returncode()  # Will raise CalledProcessError if exit != 0


default_args = {
 'owner': 'Krishna Dubey',
    'start_date': datetime(2025,5,30),
    'retries':0
}

dag=DAG(
    dag_id='etl_wikipedia_pipeline',
    default_args=default_args,
    start_date=datetime(2025, 5, 30),
    schedule_interval='@weekly',
    catchup=False,
    tags=['wikipedia','etl','pipeline']
)

#extraction from wikipedia
extract=PythonOperator(
    task_id='wikipedia_extraction',
    python_callable=wikipedia_pipeline,
    dag=dag
)

extract2=PythonOperator(
    task_id='wikipedia_extraction2',
    python_callable=wikipedia_pipeline2,
    dag=dag
)

merging=PythonOperator(
    task_id='wikipedia_merger',
    python_callable=wikipedia_pipeline3,
    dag=dag
)

upload_to_snowflake=PythonOperator(
    task_id='uploading_to_snowflake',
    python_callable=snowflake_pipeline,
    dag=dag
)



run_pentaho_transformation = PythonOperator(
    task_id='run_pentaho_transformation',
    python_callable=run_ktr
)

extract>>extract2>>merging>>upload_to_snowflake>>run_pentaho_transformation