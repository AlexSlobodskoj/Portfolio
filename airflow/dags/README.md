# ELT Orchestration with Apache Airflow & dbt

The pipeline covers the full data lifecycle: ingestion from CSV, transformation through dbt layers, data quality testing, and operational monitoring.


## Pipeline Architecture

The project consists of 9 DAGs that progressively demonstrate increasingly advanced Airflow patterns:

**Data Ingestion** — loads raw CSV data into PostgreSQL using native `COPY` command for high-speed bulk ingestion. Pre-flight checks validate both file existence and database availability before any data movement begins.

**Data Transformation** — dbt models are executed in three explicit layers: `staging → intermediate → marts`. Each layer runs as a separate Airflow task, providing granular visibility and failure isolation across the transformation chain.

**Data Quality** — `dbt test` runs automatically after every transformation to validate data integrity before downstream consumers can access the results.


## Key Technologies

| Technology | Role |
|---|---|
| Apache Airflow | DAG scheduling, task dependency management, retry logic |
| dbt | Layered SQL transformations (staging / intermediate / marts) with built-in data tests |
| PostgreSQL | Target database; health-checked via `pg_isready` before every run |
| Slack Webhooks | Real-time failure and success notifications via `on_failure_callback` |


## Airflow Patterns Demonstrated

**Dataset-driven scheduling** — `startup_pipeline_transform` triggers automatically when `startup_pipeline_load` writes to the `STARTUP_DATASET`, implementing data-aware DAG chaining without time-based polling.

**TriggerDagRunOperator** — `startup_pipeline_trigger` launches a child DAG `startup_pipeline_run` and waits for its completion before continuing, demonstrating cross-DAG orchestration.

**Jinja templating** — all credentials and paths are injected at runtime via `{{ var.value.X }}` and `{{ conn.postgres_conn.X }}`, keeping secrets out of code.

**Airflow Variables & Connections** — environment paths, database credentials, and webhook URLs managed through Airflow's secret store.

**XCom** — table name passed between `load_csv` and `save_meta` tasks for downstream reference.

**Parallel task execution** — file check and database check `[check_db, check_file] >> load_csv` run simultaneously before the load step

**Fault tolerance** — all production tasks configured with `retries=3` and `retry_delay`, plus `execution_timeout` guards against hung processes.

**Callback-based alerting** — `on_failure_callback` sends structured Slack messages with DAG name, task ID, execution date, and direct log URL.


## DAG Overview

| DAG | Schedule | Description |
|---|---|---|
| `startup_pipeline` | `0 2 * * *` | Set execution_timeout for dbt tasks |
| `startup_pipeline_load` | `0 1 * * *` | Main DAG to load CSV into PostgreSQL with Dataset output |
| `startup_pipeline_transform` | Dataset trigger | Subordinate DAG triggered by Dataset updates for run dbt tasks |
| `startup_pipeline_layers` | `0 2 * * *` | Launching 'dbt run' by layers: staging → intermediate → marts |
| `startup_pipeline_retry` | `0 2 * * *` | Full pipeline with retry logic and Slack alerts |
| `startup_pipeline_slack` | `0 2 * * *` | Pipeline with success and failure notifications in Slack  |
| `startup_pipeline_trigger` | `0 2 * * *` | Cross-DAG orchestration via TriggerDagRunOperator (main DAG) |
| `startup_pipeline_run` | Trigger | Cross-DAG orchestration via TriggerDagRunOperator (subordinate DAG) |
| `startup_pipeline_checkdb` | `0 2 * * *` | Pipeline with pre-flight database health check |


## [Continuous Integration (CI)](https://github.com/AlexSlobodskoj/Portfolio/blob/main/.github/workflows/ci.yml)

GitHub Actions workflow runs on every push:

- **Python linting** — `ruff` checks all DAG files for errors and style violations
- **DAG integrity** — Airflow `DagBag` validates that all DAGs import without errors
- **dbt parse** — both dbt projects are parsed to verify SQL syntax and `ref()` references

All three jobs run in parallel. No manual checks required.
