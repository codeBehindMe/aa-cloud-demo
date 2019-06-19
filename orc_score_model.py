# orc_score_model.py

# Author : aarontillekeratne
# Date : 2019-06-17

# This file is part of aa-cloud-demo.

# aa-cloud-demo is free software:
# you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.

# aa-cloud-demo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with aa-cloud-demo.  
# If not, see <https://www.gnu.org/licenses/>.

from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import \
    KubernetesPodOperator

from datetime import datetime, timedelta

# Constants
SERVICE_NAME = 'gcr.io/aa-cloud-demo/sample_model_dev:latest'
IMAGE_ENTRY_COMMAND = 'score'

# FIXME: Incorrect scoring data path
SCORE_DATA_COMMAND = "--scoring-file-path=gs//discovery-data-store/training-data-path/train.csv"
DAG_NAME = 'orc_score_model'

# Default arguments for the dag.
default_args = {
    'owner': 'aaron',
    'depends_on_past': False,
    'start_date': datetime(2015, 6, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(DAG_NAME, default_args=default_args,
         schedule_interval=timedelta(days=1)) as d:
    kubernetes_min_pod = KubernetesPodOperator(
        task_id="scoring_task",
        name="scoring_task",
        namespace='default',
        image=SERVICE_NAME)

