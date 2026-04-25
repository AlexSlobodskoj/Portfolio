from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.operators.nonexistent import FakeOperator

with DAG(
    dag_id='startup_pipeline',
    start_date=datetime(2024, 1, 1),
    schedule='0 2 * * *',
    catchup=False,
    description='dbt pipeline for startup analytics'
) as dag:

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command=(
            'source {{ var.value.ENV_PATH }}/bin/activate && '
            'cd {{ var.value.PROJECT_PATH }} && '
            'dbt run 2>&1'
        ),
        execution_timeout=timedelta(minutes=10)
    )

    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command=(
            'source {{ var.value.ENV_PATH }}/bin/activate && '
            'cd {{ var.value.PROJECT_PATH }} && '
            'dbt test 2>&1'
        ),
        execution_timeout=timedelta(minutes=10)
    )

    dbt_run >> dbt_test