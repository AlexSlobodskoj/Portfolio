from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id='startup_pipeline',
    start_date=datetime(2024, 1, 1),
    schedule_interval='0 2 * * *',
    catchup=False,
    description='dbt pipeline for startup analytics'
) as dag:

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command=(
            'source /Users/alexslobodskoj/Documents/GitHub/Portfolio/dbt-project/dbt-env/bin/activate && '
            'cd /Users/alexslobodskoj/Documents/GitHub/Portfolio/dbt-project/my_project && '
            'dbt run'
        )
    )

    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command=(
            'source /Users/alexslobodskoj/Documents/GitHub/Portfolio/dbt-project/dbt-env/bin/activate && '
            'cd /Users/alexslobodskoj/Documents/GitHub/Portfolio/dbt-project/my_project && '
            'dbt test'
        )
    )

    dbt_run >> dbt_test