from collections.abc import Sequence

import pytest
from seqtest.check_fib import check_fibonacci1, check_fibonacci2


def fib(n: int):
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
def test_fib1(value: Sequence[int], expected_result: bool):
    actual_result = check_fibonacci1(value)

    assert actual_result == expected_result


def test_fib2(value: Sequence[int], expected_result: bool):
    actual_result = check_fibonacci2(value)

    assert actual_result == expected_result
