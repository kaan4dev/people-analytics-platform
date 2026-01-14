from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="people_platform",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["people", "dq", "dbt"],
) as dag:

    dq_checks = BashOperator(
        task_id="dq_checks",
        bash_command="python /opt/airflow/pipelines/dq/ge_runner.py",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/airflow/dbt/people_dbt && dbt run --profiles-dir .",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/airflow/dbt/people_dbt && dbt test --profiles-dir .",
    )

    dq_checks >> dbt_run >> dbt_test