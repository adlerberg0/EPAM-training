import functools

import pytest

from hw5.save_original_info import print_result


@print_result
def custom_sum(*args):
    """This function can sum any objects which have __add___"""
    return functools.reduce(lambda x, y: x + y, args)


def test_function_save_original_params():

    assert custom_sum.__doc__ == "This function can sum any objects which have __add___"
    assert custom_sum.__name__ == "custom_sum"


def test_original_function_executes_without_printing(capsys):
    without_print = custom_sum.__original_func
    res = without_print(1, 2, 3, 4)
    stdout, err = capsys.readouterr()

    assert stdout == ""
    assert err == ""
    assert res == sum([1, 2, 3, 4])


@pytest.mark.parametrize(
    "params, expected_result",
    [
        (([1, 2, 3], [3, 2, 1]), [1, 2, 3] + [3, 2, 1]),
        ((1, 2, 3, 4, 5), sum([1, 2, 3, 4, 5])),
    ],
)
def test_function_still_works_after_decoration(params, expected_result):

    assert custom_sum(*params) == expected_result
