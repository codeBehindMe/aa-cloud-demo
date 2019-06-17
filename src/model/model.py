# model.py

# Author : aarontillekeratne
# Date : 2019-06-13

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

from abc import ABCMeta
from abc import abstractmethod
from functools import wraps
import os
from src.utils.gcs import upload_blob_from_file
import logging


class Model(metaclass=ABCMeta):

    def __init__(self):
        pass

    @abstractmethod
    def train(self, data, *args, **kwargs):
        pass

    @abstractmethod
    def predict(self, data, *args, **kwargs):
        pass

    @classmethod
    def _gcs_write_handler(cls, f):
        """
        Handles a gcp path if required.
        :return:
        """
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            args_list = list(args)
            if args_list[0].startswith("gs://"):  # FIXME: String in code
                # If its a gcp url, write to local temporarily and then move
                # it up to gcp.
                local_path = "random_string_path.mdl"  # FIXME: A lot of things
                args_list[0] = local_path
                try:
                    # Call self and persist locally.
                    f(self, *args_list, **kwargs)
                    upload_blob_from_file(args[0], local_path)
                except IOError:
                    logging.info(
                        "Bad things happened wen trying to upload file")
                finally:
                    # Make sure to remove the temporary file.
                    os.remove(local_path)
                return
            return f(self, *args, **kwargs)
        return wrapper

    @abstractmethod
    def serialise(self, path):
        pass

    @abstractmethod
    def deserialise(self, path):
        pass

    @abstractmethod
    def get_estimator(self):
        pass

    @abstractmethod
    def extract_features(self, instance):
        pass
