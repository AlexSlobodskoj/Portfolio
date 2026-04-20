from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

with DAG(
    dag_id='startup_pipeline_checkdb',
    start_date=datetime(2024, 1, 1),
    schedule='0 2 * * *',
    catchup=False,
    description='dbt pipeline with db check'
) as dag:
    # Check if PostgreSQL is available before running dbt
    check_db = BashOperator(
        task_id='check_db',
        bash_command=(
            'pg_isready -h localhost -p 5432 -U alexslobodskoj -d postgres'
        ),
        execution_timeout=timedelta(minutes=10)
    )
    # Run all dbt models: staging → intermediate → marts
    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command=(
            'source /Users/alexslobodskoj/Documents/GitHub/Portfolio/dbt-project/dbt-env/bin/activate && '
            'cd /Users/alexslobodskoj/Documents/GitHub/Portfolio/dbt-project/startups && '
            'dbt run 2>&1'
        ),
        execution_timeout=timedelta(minutes=10)
    )
    # Run dbt data quality tests after models are built
    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command=(
            'source /Users/alexslobodskoj/Documents/GitHub/Portfolio/dbt-project/dbt-env/bin/activate && '
            'cd /Users/alexslobodskoj/Documents/GitHub/Portfolio/dbt-project/startups && '
            'dbt test 2>&1'
        ),
        execution_timeout=timedelta(minutes=10)
    )
    # Pipeline order: check db → build models → validate data
    check_db >> dbt_run >> dbt_test