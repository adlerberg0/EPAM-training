from random import randrange
from typing import List

import pytest
from task4.count_zero_sum import check_sum_of_four


def get_lists(n: int) -> List[List]:
    """
    :param n: amount of numbers in each list which will result in 0
    :return: 4 list with n^4 zero sum tuples
    """
    tmp = 10
    a = [100 for _ in range(n)]
    b = [100 for _ in range(n)]
    c = [100 for _ in range(n)]
    d = [100 for _ in range(n)]
    idx = randrange(n)
    for i in range(n):
        a[idx] = tmp
        b[idx] = tmp
        c[idx] = -tmp
        d[idx] = -tmp
        idx += 1
        if idx >= n:
            idx = 0
    return [a, b, c, d]


@pytest.mark.parametrize(
    ["value", "expected_result"],
    [
        (get_lists(3), 3 ** 4),
        (get_lists(4), 4 ** 4),
        (get_lists(5), 5 ** 4),
        (get_lists(6), 6 ** 4),
    ],
)
def test_count_zero_sum(value: List[List], expected_result: int):
    actual_result = check_sum_of_four(value[0], value[1], value[2], value[3])

    assert actual_result == expected_result
