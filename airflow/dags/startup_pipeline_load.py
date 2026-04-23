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
COLUMNS = "(funding_rounds, founder_experience_years, team_size, market_size_billion, product_traction_users, burn_rate_million, revenue_million, investor_type, sector, founder_background, outcome)"
with DAG(
    dag_id='startup_pipeline_load',
    start_date=datetime(2024, 1, 1),
    schedule='0 1 * * *',
    catchup=False,
    description='Load startup data from CSV to PostgreSQL'
) as dag:
    
    # Checking for the existence of a file
    check_file = BashOperator(
        task_id='check_file',
        bash_command='ls {{ var.value.DATA_PATH }}/startup_success.csv',
        execution_timeout=timedelta(minutes=10),
        retries=3,
        retry_delay=timedelta(minutes=1),
        on_failure_callback=notify_slack_failure
    )

    # Check if PostgreSQL is available before running dbt
    check_db = BashOperator(
        task_id='check_db',
        bash_command=(
            'pg_isready -h localhost -p 5432 '
            '-U {{ var.value.DB_USER }} '
            '-d {{ var.value.DB_NAME }}'
        ),
        execution_timeout=timedelta(minutes=10),
        retries=3,
        retry_delay=timedelta(minutes=1),
        on_failure_callback=notify_slack_failure
    )

    # Load CSV into PostgreSQL using COPY — faster than pandas for large files
    # In production this would be handled by Fivetran/Airbyte
    load_csv = BashOperator(
    task_id='load_csv',
    bash_command=(
        'psql -h localhost -U {{ var.value.DB_USER }} -d {{ var.value.DB_NAME }} -c '
        '"TRUNCATE TABLE public.startup_succes;" && '
        'psql -h localhost -U {{ var.value.DB_USER }} -d {{ var.value.DB_NAME }} -c '
        '"\\COPY public.startup_succes ' + COLUMNS + ' FROM \'{{ var.value.DATA_PATH }}/startup_success.csv\' WITH (FORMAT CSV, HEADER, DELIMITER \',\');" && '
        'echo "startup_success.csv|public.startup_succes"'
    ),
    do_xcom_push=True,
    execution_timeout=timedelta(minutes=10),
    retries=3,
    retry_delay=timedelta(minutes=1),
    on_failure_callback=notify_slack_failure,
    outlets=[STARTUP_DATASET]
    )

    # Save the table name for the next DAG
    save_meta = BashOperator(
        task_id='save_meta',
        bash_command='airflow variables set last_loaded_table public.startup_success'
    )

    # Send success notification when all tasks complete
    notify_success = BashOperator(
        task_id='notify_success',
        bash_command=(
            'python3 -c "'
            'import requests; '
            'xcom_val = \'{{ ti.xcom_pull(task_ids="load_csv") }}\'; '
            'f_name, t_name = xcom_val.split(chr(124)); '
            'requests.post(\'{{ var.value.SLACK_WEBHOOK_URL }}\', '
            'json={\'text\': f\':large_green_circle: File *{f_name}* downloaded in table *{t_name}*\\n'
            'DAG: *{{ dag.dag_id }}*\'}, timeout=10)"'
        ),
        execution_timeout=timedelta(minutes=1),
        retries=3,
        retry_delay=timedelta(minutes=1)
    )

    # Pipeline order: check db → load csv → notify
    [check_db, check_file] >> load_csv >> save_meta >> notify_success