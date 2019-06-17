# data_generator.py

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

"""
Generates a bunch of data with some function and some noise.
"""
import numpy as np


def function(i, j, k, mu, sigma):
    """
    Returns a function with parameters i, j ,k and error with mean mu and
    standard deviation sigma.
    :param i:
    :param j:
    :param k:
    :param mu:
    :param sigma:
    :return:
    """

    def generator(x, y, z):
        """
        Generates the value of the outer function.
        :param x:
        :param y:
        :param z:
        :return:
        """
        return (i * x + j * y + k * z) + np.random.normal(mu, sigma)

    return generator


def generate(f_weights: list, mu, sigma, k_max):
    """
    Generate a values with underlying function.
    :param f_weights:
    :param mu:
    :param sigma:
    :param k_max:
    :return:
    """
    f = function(*f_weights, mu, sigma)
    while True:
        x, y, z = np.random.randint(k_max, size=3).tolist()
        label = f(x, y, z)
        yield x, y, z, label


if __name__ == '__main__':

    # Generate a file with data

    i_max = 10000
    i = 0
    with open('train.csv', 'w+') as f:
        for instance in generate([2, 3, 4], 3, 3, 25):
            f.write(f"{','.join(map(str, instance))}\n")
            i += 1
            if i == i_max:
                break

    i = 0
    with open('tests.csv', 'w+') as f:
        for instance in generate([2, 3, 4], 3, 3, 25):
            f.write(f"{','.join([str(x) for x in instance][:-1])}\n")
            i += 1
            if i == i_max:
                break
