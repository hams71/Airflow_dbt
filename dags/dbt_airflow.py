import pendulum
from airflow import DAG
from airflow_dbt.operators.dbt_operator import (
    DbtSeedOperator,
    DbtSnapshotOperator,
    DbtRunOperator,
    DbtDepsOperator,
    DbtDocsGenerateOperator
)
from airflow.utils.dates import days_ago

default_args = {
  'dir': '/home/ubuntu/airflow/dbt_project/',
  #'start_date': days_ago(0)
}

with DAG(dag_id='dbt', default_args=default_args, schedule_interval='@daily', start_date=pendulum.datetime(2022, 10, 13, tz="UTC")) as dag:

  """
  The seed operator will allow us to load data file from local system to snowflake using dbt
  """
  dbt_seed = DbtSeedOperator(
    task_id='dbt_seed',
  )

  """
  The snapshot operator will capture changes SCD-2 for some of the models
  """
  dbt_snapshot = DbtSnapshotOperator(
    task_id='dbt_snapshot',
  )
  """
  The run operator will load the seeded files to some other tables with transformations
  """
  dbt_run = DbtRunOperator(
    task_id='dbt_run',
    select='Core',
    full_refresh=True,
  )

  """
  This operator used to install some dbt-utils if running for the first time
  """
  dbt_deps = DbtDepsOperator(
    task_id='dbt_deps',
  )

  """
  Docs Operator will generate a new update file on which we can see the changes in UI
  """
  dbt_docs = DbtDocsGenerateOperator(
    task_id='dbt_docs',
  )

  # dbt_test = DbtTestOperator(
  #   task_id='dbt_test',
  #   retries=0,  # Failing tests would fail the task, and we don't want Airflow to try again
  # )


  dbt_deps >> dbt_seed >> dbt_run >> dbt_snapshot >> dbt_docs