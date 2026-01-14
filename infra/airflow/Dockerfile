FROM apache/airflow:2.10.3-python3.11

USER airflow
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

CMD ["bash", "-lc", "airflow db check || airflow db init; airflow db migrate; airflow users create \
  --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com || true; \
  airflow webserver & airflow scheduler"]
