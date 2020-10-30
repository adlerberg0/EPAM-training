"""
Given a cell with "it's a fib sequence" from slideshow,
    please write function "check_fib",
    which accepts a Sequence of integers, and
    returns if the given sequence is a Fibonacci sequence
We guarantee, that the given sequence contain >= 0 integers inside.
"""
from collections.abc import Sequence
from math import sqrt


def check_fibonacci2(data: Sequence[int]) -> bool:
    res = True
    prev1 = 0
    prev2 = 0
    for i, item in enumerate(data):
        if i == 0 or i == 1:
            if item != 0:
                res = False
                break
        elif i == 1:
            if item != 1:
                res = False
        if item != prev1 + prev2:
            res = False
            break
        prev2 = prev1
        prev1 = item
    return res


def _binet_formula(n: int) -> int:
    return int((((1 + sqrt(5)) / 2) ** n - ((1 - sqrt(5)) / 2) ** n) / sqrt(5))


def check_fibonacci1(data: Sequence[int]) -> bool:
    res = True
    for i, item in enumerate(data):
        if item != int(_binet_formula(i)):
            res = False
            break
    return res
