# demopipeline.py

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

import logging

import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.io import WriteToText
from apache_beam.transforms import BatchElements

from src.model.linear_model import LinearModelNoRegularisation
from src.pipelines.mlpipeline import MLPipeline
from src.pipelines.mlpipeline import ModelModeKey
from src.pipelines.mlpipeline import PersistenceModeKey
from src.utils.beam_utils import beam_runner_args_parser


class TrainModel(beam.DoFn):

    def __init__(self, model, *unused_args, **unused_kwargs):
        super().__init__(*unused_args, **unused_kwargs)
        self._model = model

    def process(self, element, *args, **kwargs):
        self._model.train(element)


class LinearRegressionPipeline(MLPipeline):

    def __init__(self, file_path, model_path, model_mode, pers_mode,
                 beam_runner, max_batch_size, min_batch_size,
                 output_path=None):
        super().__init__(model_mode, pers_mode, beam_runner, max_batch_size,
                         min_batch_size)
        self.file_path = file_path
        self.model_path = model_path
        self.model = LinearModelNoRegularisation()
        if model_mode == ModelModeKey.SCORE:
            self.model.deserialise(model_path)
        self.output_path = output_path

    def execute(self):
        """
        Executes the training pipeline
        :return:
        """

        p_opts = PipelineOptions([beam_runner_args_parser(self.beam_runner)])
        p_opts.view_as(SetupOptions).save_main_session = True

        with beam.Pipeline(options=p_opts) as p:
            p = p | ReadFromText(self.file_path)
            p = p | beam.Map(lambda x: x.split(','))
            if not self.max_batch_size == -1:
                p = p | BatchElements(self.min_batch_size, self.max_batch_size)
            if self.model_mode == ModelModeKey.TRAIN:
                p = p | beam.Map(lambda x: self.model.train(x))
            if self.model_mode == ModelModeKey.SCORE:
                p = p | beam.Map(lambda x: self.model.predict(x))
                if self.pers_mode == PersistenceModeKey.WET:
                    p | WriteToText(self.output_path)

        if self.pers_mode == PersistenceModeKey.WET and \
                self.model_mode == ModelModeKey.TRAIN:
            logging.info("Serialising model")
            self.model.serialise(self.model_path)
