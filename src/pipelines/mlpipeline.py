# pipeline.py

# Author : aarontillekeratne
# Date : 2019-06-19

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

from enum import Enum


class ModelModeKey(Enum):
    TRAIN = 1
    VALIDATION = 2
    SCORE = 3


class PersistenceModeKey(Enum):
    DRY = 0
    WET = 1


class MLPipeline(metaclass=ABCMeta):

    def __init__(self, model_mode, pers_mode, beam_runner, max_batch_size,
                 min_batch_size):
        self.model_mode = model_mode
        self.pers_mode = pers_mode
        self.beam_runner = beam_runner
        self.max_batch_size = max_batch_size
        self.min_batch_size = min_batch_size

    @abstractmethod
    def execute(self):
        pass
