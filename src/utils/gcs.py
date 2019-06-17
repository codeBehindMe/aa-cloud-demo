# gcs.py

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

from google.cloud import storage
import logging
from urllib.parse import urlparse


def upload_blob_from_file(target_loc, source_file_name):
    """
    Uploads a file to a bucket.
    https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python1
    :param source_file_name:
    :param destination_blob_name:
    :return:
    """

    storage_client = storage.Client()

    parsed = urlparse(target_loc)

    bucket = storage_client.get_bucket(parsed.netloc)
    # FIXME: Ugly
    if parsed.path.startswith("/"):
        parsed_path = parsed.path[1:]
    else:
        parsed_path = parsed.path
    blob = bucket.blob(parsed_path)
    blob.upload_from_filename(source_file_name)

    logging.info(f"Successfully uploaded to {target_loc}")
