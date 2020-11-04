from random import randrange
from typing import List

import pytest
from task5.max_sum import find_maximal_sub_array_sum


def get_list(max_list: int, list_len: int) -> List:
    """
    :param max_list: embed this list in row in result list
    :param list_len: len of result list
    :return: res list with embedded max_list
             (other values are less than min(max_list))
    """
    k = len(max_list)
    res = [0] * list_len
    min_value = min(max_list)
    idx_set = set()
    idx = randrange(k)
    # get k random idx in row
    for i in range(k):
        idx_set.add(idx)
        idx += 1
        if idx >= list_len:
            idx = 0
    # fill with random numbers less than min_value from max list
    for i in range(list_len):
        if i in idx_set:
            res[i] = max_list.pop()
        else:
            res[i] = randrange(-1000000000, min_value)
    return res, k


@pytest.mark.parametrize(
    ["value", "expected_result"],
    [
        (get_list([10, 12, 15], 10), sum([10, 12, 15])),
        (get_list([30, 40, 50], 20), sum([30, 40, 50])),
        ([[1, 1, -1, 10, 3, 2, 1], 3], 15),
        ([[100, 1, -1, 10, 3, 2, 1], 3], 101),
        (get_list([-10, -30, -50], 100), -10),
        (get_list([-1, -3, -50], 100), -1),
        (get_list([-10, -30, -50], 100), -10),
        (get_list([-1, -3, -50], 100), -1),
    ],
)
def test_count_zero_sum(value: List[List], expected_result: int):
    actual_result = find_maximal_sub_array_sum(value[0], value[1])

    assert actual_result == expected_result
