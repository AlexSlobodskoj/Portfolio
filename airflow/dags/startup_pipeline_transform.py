from airflow import DAG, Dataset
from airflow.operators.bash import BashOperator
from airflow.models import Variable
from datetime import datetime, timedelta
import requests

def notify_slack_failure(context):
    webhook_url = Variable.get('SLACK_WEBHOOK_URL')
    task_id = context['task_instance'].task_id
    dag_id = context['task_instance'].dag_id
    execution_date = context['execution_date']
    log_url = context['task_instance'].log_url

    message = {
        "text": (
            f":red_circle: *Task failed*\n"
            f"*DAG:* {dag_id}\n"
            f"*Task:* {task_id}\n"
            f"*Date:* {execution_date}\n"
            f"*Logs:* {log_url}"
        )
    }
    requests.post(webhook_url, json=message)

STARTUP_DATASET = Dataset("postgres://public/startup_succes")

with DAG(
    dag_id='startup_pipeline_transform',
    schedule=[STARTUP_DATASET],
    start_date=datetime(2024, 1, 1),
    catchup=False,
    description='Run dbt transformations after CSV load'
) as dag:

    # Check if PostgreSQL is available before running dbt
    check_db = BashOperator(
        task_id='check_db',
        bash_command=(
            'pg_isready -h localhost -p 5432 -U alexslobodskoj -d postgres'
        ),
        execution_timeout=timedelta(minutes=10),
        retries=3,
        retry_delay=timedelta(minutes=1),
        on_failure_callback=notify_slack_failure
    )

    # Run staging layer models
    dbt_run_staging = BashOperator(
        task_id='dbt_run_staging',
        bash_command=(
            'source /Users/alexslobodskoj/Documents/GitHub/Portfolio/dbt-project/dbt-env/bin/activate && '
            'cd /Users/alexslobodskoj/Documents/GitHub/Portfolio/dbt-project/startups && '
            'dbt run --select staging 2>&1'
        ),
        execution_timeout=timedelta(minutes=10),
        retries=3,
        retry_delay=timedelta(minutes=1),
        on_failure_callback=notify_slack_failure
    )
    # Run marts layer models
    dbt_run_int = BashOperator(
        task_id='dbt_run_int',
        bash_command=(
            'source /Users/alexslobodskoj/Documents/GitHub/Portfolio/dbt-project/dbt-env/bin/activate && '
            'cd /Users/alexslobodskoj/Documents/GitHub/Portfolio/dbt-project/startups && '
            'dbt run --select intermediate 2>&1'
        ),
        execution_timeout=timedelta(minutes=10),
        retries=3,
        retry_delay=timedelta(minutes=1),
        on_failure_callback=notify_slack_failure
    )

    # Run marts layer models
    dbt_run_marts = BashOperator(
        task_id='dbt_run_marts',
        bash_command=(
            'source /Users/alexslobodskoj/Documents/GitHub/Portfolio/dbt-project/dbt-env/bin/activate && '
            'cd /Users/alexslobodskoj/Documents/GitHub/Portfolio/dbt-project/startups && '
            'dbt run --select marts 2>&1'
        ),
        execution_timeout=timedelta(minutes=10),
        retries=3,
        retry_delay=timedelta(minutes=1),
        on_failure_callback=notify_slack_failure
    )

    # Run dbt data quality tests after models are built
    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command=(
            'source /Users/alexslobodskoj/Documents/GitHub/Portfolio/dbt-project/dbt-env/bin/activate && '
            'cd /Users/alexslobodskoj/Documents/GitHub/Portfolio/dbt-project/startups && '
            'dbt test 2>&1'
        ),
        execution_timeout=timedelta(minutes=10),
        retries=3,
        retry_delay=timedelta(minutes=1),
        on_failure_callback=notify_slack_failure
    )

    # Send success notification when all tasks complete
    notify_success = BashOperator(
        task_id='notify_success',
        bash_command=(
            'python3 -c "'
            'from airflow.models import Variable; '
            'import requests; '
            'webhook = Variable.get(\'SLACK_WEBHOOK_URL\'); '
            'requests.post(webhook, json={\'text\': \':large_green_circle: *Pipeline completed successfully*\\n*DAG:* startup_pipeline_transform\\nAll models built and tests passed.\'}, timeout=10)'
            '"'
        ),
        execution_timeout=timedelta(minutes=1),
        retries=3,
        retry_delay=timedelta(minutes=1)
    )

    # Pipeline order: check db → staging → marts → test → notify
    check_db >> dbt_run_staging >> dbt_run_int >> dbt_run_marts >> dbt_test >> notify_success