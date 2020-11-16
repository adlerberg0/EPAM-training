import pytest

from hw3.task4.hw4 import is_armstrong


@pytest.mark.parametrize("value, result", [(153, True)])
def test_is_armstrong_true(value: int, result: bool):
    assert is_armstrong(value) is result


@pytest.mark.parametrize("value, result", [(10, False)])
def test_is_armstrong_false(value: int, result: bool):
    assert is_armstrong(value) is result
