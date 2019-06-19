# orchestration.py

# Author : aarontillekeratne
# Date : 2019-06-12

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
from airflow.models import Variable

from datetime import datetime, timedelta

# Constants
DAG_NAME = "orc_train_model"
IMAGE_ENTRY_COMMAND = "train"

# Environment
env_id = Variable.get("env")
# noinspection PyPep8
TRAIN_DATA_COMMAND = f"""--train-file-path=gs://{env_id}-data-store/training-data-path/train.csv"""
MODEL_OUTPUT_PATH_COMMAND = f"""--model-save-path=gs://{env_id}-data-store/models/"""

# Default arguments for the dag.
default_args = {
    'owner': 'aaron',
    'depends_on_past': False,
    'start_date': datetime(2015, 6, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

with DAG(DAG_NAME, default_args=default_args,
         schedule_interval=None) as d:
    kubernetes_min_pod = KubernetesPodOperator(
        namespace='default',
        task_id="train-task",
        name="train-task",
        arguments=['train', TRAIN_DATA_COMMAND, MODEL_OUTPUT_PATH_COMMAND],
        image='gcr.io/aa-cloud-demo/sample_model_dev:latest')
