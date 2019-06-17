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

from datetime import datetime, timedelta

# Constants
IMAGE_NAME = "gcr.io/aa-cloud-demo/sample-model"
IMAGE_ENTRY_COMMAND = "train"

# noinspection PyPep8
TRAIN_DATA_COMMAND = f"""--train-file-path=gs://discovery-data-store/training-data-path/"""
MODEL_OUTPUT_PATH_COMMAND = f"""--model-save-path=gs:/discovery-data-store/models/"""

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

with DAG(IMAGE_NAME, default_args=default_args,
         schedule_interval=timedelta(days=1)) as d:
    kubernetes_min_pod = KubernetesPodOperator(
        # The ID specified for the task.
        task_id=f"{IMAGE_NAME}_TRAIN_TASK",
        # Name of task you want to run, used to generate Pod ID.
        name=f"{IMAGE_NAME}_TRAIN_TASK",
        # Entrypoint of the container, if not specified the Docker container's
        # entrypoint is used. The cmds parameter is templated.
        cmds=[IMAGE_ENTRY_COMMAND, TRAIN_DATA_COMMAND
            , MODEL_OUTPUT_PATH_COMMAND],
        # The namespace to run within Kubernetes, default namespace is
        # `default`. There is the potential for the resource starvation of
        # Airflow workers and scheduler within the Cloud Composer environment,
        # the recommended solution is to increase the amount of nodes in order
        # to satisfy the computing requirements. Alternatively, launching pods
        # into a custom namespace will stop fighting over resources.
        namespace='default',
        # Docker image specified. Defaults to hub.docker.com, but any fully
        # qualified URLs will point to a custom repository. Supports private
        # gcr.io images if the Composer Environment is under the same
        # project-id as the gcr.io images.
        image=IMAGE_NAME)
