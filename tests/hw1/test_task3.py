import os
from collections.abc import Sequence
from random import randrange
from typing import Tuple

import pytest

from hw1.task3.extrema import find_maximum_and_minimum


def gen_file(name: str, nums: Sequence[int], count: int) -> str:
    """
    :param name:  name of new file with test data
    :param nums:  arr with min and max values of test data
    :param count: amount of test samples in file
    :return: name of just created file
    """
    f = open(name, "w")
    min_val = nums[0]
    max_val = nums[1]
    min_idx = randrange(count - 1)
    max_idx = randrange(count - 1)
    if min_idx == max_idx:
        max_idx += 1
        if max_idx > count:
            max_idx = 0
    for i in range(count):
        if i == min_idx:
            f.write(f"{min_val} \n")
        elif i == max_idx:
            f.write(f"{max_val} \n")
        else:
            f.write(f"{randrange(min_val, max_val)} \n")
    f.close()
    return name


@pytest.mark.parametrize(
    ["value", "expected_result"],
    [
        (gen_file("test1.txt", [0, 10], 5), (0, 10)),
        (gen_file("test2.txt", [-100, 100], 10), (-100, 100)),
        (gen_file("test3.txt", [0, 100000000], 100), (0, 100000000)),
        (gen_file("test4.txt", [-100000000, 0], 100), (-100000000, 0)),
    ],
)
def test_extrema(value: str, expected_result: Tuple[int, int]):
    actual_result = find_maximum_and_minimum(value)
    # del test file
    os.remove(value)

    assert actual_result == expected_result
