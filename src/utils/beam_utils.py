# beam_utils.py

# Author : aarontillekeratne
# Date : 2019-08-20

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


ARG_MAP_PREFIX = '--runner='  # Required by beam pipeline options
args_map = {"direct": "DirectRunner"}


def beam_runner_args_parser(arg: str) -> str:
    """
    Converts the string arguments that are coming from the command line to the
    format that the pipeline options expects it to be in.
    :param arg: String argument
    :return:
    """
    return f"{ARG_MAP_PREFIX}{args_map[arg]}"
