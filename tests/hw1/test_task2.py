from typing import Iterable, Sequence

import pytest

from hw1.task2.check_fib import check_fibonacci1, check_fibonacci2


def fib(n: int) -> Iterable:
    """
    fib number generator
    """
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


@pytest.mark.parametrize(
    ["value", "expected_result"],
    [
        (list(fib(1)), True),
        (list(fib(2)), True),
        (list(fib(3)), True),
        (list(fib(4)), True),
        (list(fib(5)), True),
        (list(fib(6)), True),
        (list(fib(7)), True),
        (list(fib(4)) + [-1], False),
        (list(fib(5)) + list(fib(5)), False),
        ([-1] + list(fib(6)), False),
    ],
)
def test_fib(value: Sequence[int], expected_result: bool):
    # test 2 alternative functions
    actual_result1 = check_fibonacci1(value)
    actual_result2 = check_fibonacci2(value)
    result = actual_result1 == expected_result and actual_result2 == expected_result
    assert result
