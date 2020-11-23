import os
from typing import Any

import pytest

from hw4.task1.hw1 import read_magic_number


@pytest.fixture
def create_tmp_file(request):
    file_name, value = request.param
    with open(file_name, "w") as f:
        f.write(str(value))
    yield file_name
    os.remove(file_name)


@pytest.mark.parametrize(
    "create_tmp_file, expected_result",
    [
        (("text1.txt", "1"), True),
        (("text2.txt", "-3"), False),
        (("text3.txt", "some data"), "Exception"),
    ],
    indirect=["create_tmp_file"],
)
def test_read_magic_number(create_tmp_file: str, expected_result: Any):
    file_name = create_tmp_file
    if expected_result == "Exception":
        with pytest.raises(ValueError):
            read_magic_number(file_name)
    else:
        assert read_magic_number(file_name) == expected_result
