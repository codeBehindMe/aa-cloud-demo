# linear_model.py

# Author : aarontillekeratne
# Date : 2019-06-14

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


import logging
from sklearn.linear_model import SGDRegressor
from sklearn.externals import joblib
from src.model.model import Model

import numpy as np


# FIXME: Is it smart just persisting the estimator? Maybe entire object model?

class LinearModelNoRegularisation(Model):

    def __init__(self):
        super().__init__()
        self._estimator = SGDRegressor()

    def train(self, data, *args, **kwargs):
        x = data[: -1]  # Features are everything but the last element.
        y = np.array(data[-1]).reshape(-1)  # Last element is the label.
        x = np.array(x).reshape(1, -1)

        logging.info(f"fitting x: {x} y: {y}")
        self._estimator.partial_fit(x, y)

    def predict(self, data, *args, **kwargs):
        x = data[: -1]  # Features are everything but the last element.

        logging.info(f"predicting x: {x}")
        return self._estimator.predict(x)

    @Model._default_name_handler
    @Model._gcs_write_handler
    def serialise(self, path):
        joblib.dump(self._estimator, path)

    def deserialise(self, path):
        self._estimator = joblib.load(path)

    def get_estimator(self):
        return self._estimator

    def extract_features(self, instance):
        return instance
