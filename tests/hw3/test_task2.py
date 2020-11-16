from time import perf_counter
from typing import Callable

import pytest

from hw3.task2.hw2 import call_func


@pytest.mark.parametrize("func, time_setpoint", [(call_func, 60)])
def test_multithreading(func: Callable, time_setpoint: int):
    if __name__ == "__main__":
        t1 = perf_counter()
        call_func(list(range(0, 501)))
        t2 = perf_counter()

        assert t2 - t1 < time_setpoint
