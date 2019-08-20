# main.py

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

from argparse import ArgumentParser
import logging

import pytest
from src.pipelines.linearregressionpipeline import LinearRegressionPipeline
from src.pipelines.mlpipeline import ModelModeKey, PersistenceModeKey

logging_map = {'info': logging.INFO
    , 'debug': logging.DEBUG
    , 'warn': logging.WARN
    , 'error': logging.ERROR
    , 'critical': logging.CRITICAL}

# FIXME: This should be a hierarchical argument parser.
parser = ArgumentParser()

parser.add_argument('mode', action='store', choices=['train', 'score', 'test'])

# Arguments for training mode.
parser.add_argument('--train-file-path', action='store', required=False)
parser.add_argument('--model-save-path', action='store', required=False)

# Arguments for scoring mode.
parser.add_argument('--scoring-file-path', action='store', required=False)
parser.add_argument('--model-path', action='store', required=False)
parser.add_argument('--score-output-path', action='store', required=False)

# general arguments
parser.add_argument('--log-level', action='store',
                    choices=['debug', 'info', 'warn', 'error',
                             'critical'], default='info')

parser.add_argument('--beam-runner', action='store')
parser.add_argument('--max-batch-size', action='store', type=int, default=-1)
parser.add_argument('--min-batch-size', action='store', type=int, default=1)


# FIXME: Move to utilities.
# FIXME: This shouldn't be handled lke this.
def check_args_not_none(*args):
    if None in args:
        raise ValueError()


if __name__ == '__main__':
    args = parser.parse_args()
    logging.getLogger().setLevel(logging.INFO)

    if args.mode == 'train':
        # FIXME: Use hierarchical argument parser.
        check_args_not_none(args.train_file_path, args.model_save_path
                            , args.beam_runner)

        tr_pipe = LinearRegressionPipeline(file_path=args.train_file_path
                                           , model_path=args.model_save_path
                                           , model_mode=ModelModeKey.TRAIN
                                           , pers_mode=PersistenceModeKey.WET
                                           , beam_runner=args.beam_runner)

        tr_pipe.execute()

    elif args.mode == 'score':
        # FIXME: Use hierarchical argument parser.

        check_args_not_none(args.scoring_file_path, args.model_path,
                            args.score_output_path, args.beam_runner)
        score_pipe = \
            LinearRegressionPipeline(file_path=args.train_file_path
                                     , model_path=args.model_save_path
                                     , model_mode=ModelModeKey.SCORE
                                     , pers_mode=PersistenceModeKey.WET
                                     , output_path=args.score_output_path
                                     , beam_runner=args.beam_runner)
        score_pipe.execute()

    elif args.mode == 'test':
        pytest.main(['-x', 'tests'])
