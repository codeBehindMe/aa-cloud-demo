# aarons_xgb_model.py

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

import xgboost as xgb
from src.model.model import Model


class AaronsAwesomeXgbModel(Model):

    def extract_features(self, instance):
        pass

    def serialise(self, path):
        pass

    def deserialise(self, path):
        pass

    def get_estimator(self):
        return self.bst

    def train(self, data, *args, **kwargs):
        d_mat = xgb.DMatrix(data)
        if self.bst is None:
            self.bst = xgb.train(self.params, d_mat, 1)
        else:
            self.bst = xgb.train(self.params, d_mat, 1, xgb_model=self.bst)

    def predict(self, data, *args, **kwargs):
        pass

    def __init__(self):
        super().__init__()
        self.params = {'max_depth': 2, 'eta': 1, 'silent': 1,
                       'objective': 'binary:logistic'}
        self.n_rounds = 2
        self.bst = None

