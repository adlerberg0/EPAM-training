from typing import Any
from unittest.mock import Mock, patch

import pytest

from hw4.task2.hw2 import count_dots_on_i


@pytest.mark.parametrize(
    "html_page, expected_result",
    [
        (b"<p>Hello world!<p>", 0),
        (b"<p> i i i<p>", 3),
        (b"<p> raise exception <p>", "Exception"),
    ],
)
@patch("urllib.request.urlopen")
def test_count_dots_on_i(mock_request, html_page: str, expected_result: Any):
    if expected_result == "Exception":
        mock_request.return_value = Mock(
            read=Mock(side_effect=Exception("I did smth and it doesn't work now("))
        )
        with pytest.raises(ValueError):
            count_dots_on_i("www.foo.com")
    else:
        mock_request.return_value = Mock(read=Mock(return_value=html_page))
        assert count_dots_on_i("www.foo.com") == expected_result
