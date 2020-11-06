"""
Given a cell with "it's a fib sequence" from slideshow,
    please write function "check_fib",
    which accepts a Sequence of integers, and
    returns if the given sequence is a Fibonacci sequence
We guarantee, that the given sequence contain >= 0 integers inside.
"""
from collections.abc import Sequence
from math import sqrt


def check_fibonacci1(data: Sequence[int]) -> bool:
    """
    normal way to check fib sequence
    """
    res = True
    num_1 = 0
    num_2 = 1
    while data[0] > num_1:
        num_1, num_2 = num_2, num_1 + num_2
    for i, item in enumerate(data):
        if item != num_1:
            res = False
            break
        num_1, num_2 = num_2, num_1 + num_2

    return res


def _binet_formula(n: int) -> int:
    return int((((1 + sqrt(5)) / 2) ** n - ((1 - sqrt(5)) / 2) ** n) / sqrt(5))


def check_fibonacci2(data: Sequence[int]) -> bool:
    """
    I was curious if this works
    """
    res = True
    for i, item in enumerate(data):
        if item != int(_binet_formula(i)):
            res = False
            break
    return res
