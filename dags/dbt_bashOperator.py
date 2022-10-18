from anyio import TASK_STATUS_IGNORED
import pendulum
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago, datetime, timedelta

args = {
  'dir': '/home/ubuntu/airflow/dbt_project/'
}

DIR = '/home/ubuntu/airflow/dbt_project/'

with DAG(
    dag_id='dbt_dag_bash',
    start_date=datetime(2022, 10, 13),
    description='An Airflow DAG to invoke simple dbt commands',
    #schedule_interval=timedelta(days=1),
    schedule_interval=timedelta(days=1),
    default_args=args
) as dag:


    change_dir = BashOperator(
        task_id='dbt_project',
        bash_command='cd /home/ubuntu/airflow/dbt_project/'
    )

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command=f'cd {DIR} && dbt run -m Core'
    )

    dbt_seed = BashOperator(
        task_id='dbt_seed',
        bash_command=f'cd {DIR} && dbt seed --full-refresh'
    )

    dbt_snapshot = BashOperator(
        task_id='dbt_snapshot',
        bash_command=f'cd {DIR} && dbt snapshot'
    )

    # dbt_deps = BashOperator(
    #     task_id='dbt_deps',
    #     bash_command='dbt deps'
    # )

    dbt_docs = BashOperator(
        task_id='dbt_docs',
        bash_command=f'cd {DIR} && dbt docs generate'
    )


    change_dir >> dbt_seed >> dbt_run >> dbt_snapshot >> dbt_docs