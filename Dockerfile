FROM apache/airflow:2.7.1-python3.9

COPY requirements.txt /opt/airflow/

USER root
RUN apt-get update && apt-get install -y gcc python3-dev

# Install Java
RUN apt-get update && apt-get install -y default-jre && rm -rf /var/lib/apt/lists/*
# Set up Pentaho directory
COPY data-integration /opt/data-integration
COPY transformation/Transformation1Movies.ktr /opt/transformation/Transformation1Movies.ktr

# Permissions and logging
RUN chmod +x /opt/data-integration/pan.sh \
 && mkdir -p /opt/data-integration/.kettle \
 && mkdir -p /opt/data-integration/logs \
 && chmod -R 777 /opt/data-integration/logs

USER airflow

RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt
