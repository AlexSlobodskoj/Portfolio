from airflow import DAG
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

with DAG(
    dag_id='startup_pipeline_run',
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    description='dbt run intermediate & marts'
) as dag:

    # Run intermediate layer models only
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

    # Run marts layer models only
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

    # Send success notification when all tasks complete
    notify_success = BashOperator(
        task_id='notify_success',
        bash_command=(
            'python3 -c "'
            'from airflow.models import Variable; '
            'import requests; '
            'webhook = Variable.get(\'SLACK_WEBHOOK_URL\'); '
            'requests.post(webhook, json={\'text\': \':large_green_circle: *Pipeline completed successfully*\\n*DAG:* startup_pipeline_run\\nAll models built and tests passed.\'}, timeout=10)'
            '"'
        ),
        execution_timeout=timedelta(minutes=1),
        retries=3,
        retry_delay=timedelta(minutes=1)
    )

    # Pipeline order: int → marts → notify
    dbt_run_int >> dbt_run_marts >> notify_success