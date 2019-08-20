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
import datetime


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
        # FIXME: Is this the best way to do this?
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
                local_path = os.path.basename(args[0])
                args_list[0] = local_path
                try:
                    # Call self and persist locally.
                    f(self, *args_list, **kwargs)
                    upload_blob_from_file(args[0], local_path)
                except IOError:
                    # FIXME: Bad logging info.
                    logging.info(
                        "Bad things happened when trying to upload file")
                finally:
                    # Make sure to remove the temporary file.
                    os.remove(local_path)
                return
            return f(self, *args, **kwargs)

        return wrapper

    @classmethod
    def _default_name_handler(cls, f):
        # FIXME: Is this the best way to do this?
        """
        If an explicit model name isn't given, this generates a model name
        to be written.
        :param f:
        :return:
        """

        @wraps(f)
        def wrapper(self, *args, **kwargs):
            # If the base name is defined, no action required.
            if os.path.basename(args[0]) != '':
                return f(self, *args, **kwargs)

            # Else generate a filename
            args_list = list(args)
            cls_name = self.__class__.__name__
            ts = round(datetime.datetime.now().timestamp())
            f_name = f"{ts}_{cls_name}"
            args_list[0] = os.path.join(args[0], f_name)
            return f(self, *args_list, **kwargs)

        return wrapper

    @classmethod
    def _gcs_read_handler(cls, f):
        """
        Handles when reading from gcs.
        :param f:
        :return:
        """

        @wraps(f)
        def wrapper(self, *args, **kwargs):
            args_list = list(args)

            # FIXME: String in code.
            if args[0].startswith('gs://'):
                raise NotImplementedError()

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
