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

import subprocess
# from src.pipelines.train_pipeline import TrainingPipeline

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


def check_args_not_none(*args):
    if None in args:
        raise ValueError()


if __name__ == '__main__':
    args = parser.parse_args()

    if args.mode == 'train':
        # FIXME: Use hierarchical argument parser.
        check_args_not_none(args.train_file_path, args.model_save_path)

        # tr_pipe = TrainingPipeline(file_path=args.train_file_path
        #                            , model_output_path=args.model_save_path)
        #
        # tr_pipe.execute()

    elif args.mode == 'score':
        # FIXME: Use hierarchical argument parser.

        check_args_not_none(args.scoring_file_path, args.model_path,
                            args.score_output_path)

    elif args.mode == 'test':
        print("it_works")
        # subprocess.run(['pytest'])
