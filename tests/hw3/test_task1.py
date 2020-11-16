from io import StringIO
from typing import Callable

import pytest

from hw3.task1.hw1 import cache


def f():
    return input("? ")  # careful with input() in python2, use raw_input() instead


@pytest.mark.parametrize("func, times, repeat_pls", [(f, 1, 3), (f, 10, 2), (f, 30, 1)])
def test_cache(monkeypatch, capsys, func: Callable, times: int, repeat_pls: int):
    decorated = cache(times)(func)
    test_str = f"{times}"
    number_inputs = StringIO(test_str)
    monkeypatch.setattr("sys.stdin", number_inputs)
    for i in range((times + 1) * repeat_pls):
        number_inputs.seek(0)
        if i % (times + 1) == 0:
            number_inputs.seek(0)
            res = decorated()
            # resume capture after question have been asked
            captured = capsys.readouterr()

            assert captured.out == "? "
            assert res == test_str
        else:
            res = decorated()
            captured = capsys.readouterr()

            assert captured.out == ""
            assert res == test_str
