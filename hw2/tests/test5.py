import string
from typing import Any, Sequence

import pytest
from task5.hw5 import custom_range


@pytest.mark.parametrize(
    ["chars", "args", "expected_result"],
    [
        (string.ascii_lowercase, ["g"], ["a", "b", "c", "d", "e", "f"]),
        (
            string.ascii_lowercase,
            ["g", "p"],
            ["g", "h", "i", "j", "k", "l", "m", "n", "o"],
        ),
        (string.ascii_lowercase, ["p", "g", -2], ["p", "n", "l", "j", "h"]),
    ],
)
def test_task4(
    chars: Sequence[Any], args: Sequence[Any], expected_result: Sequence[Any]
):
    actual_result = custom_range(chars, *args)
    assert actual_result == expected_result
