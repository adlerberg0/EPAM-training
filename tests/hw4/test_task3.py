import pytest

from hw4.task3.hw3 import my_precious_logger


@pytest.mark.parametrize(
    "string_to_log",
    [
        "OK",
        "error: expected a ';'",
        "error: identifier 'tmp' is undefined",
        "error: too many arguments in function call",
        "error: 'var' has already been declared in the current scope",
    ],
)
def test_my_precious_logger(capsys, string_to_log: str):
    if string_to_log.startswith("error:"):
        my_precious_logger(string_to_log)

        assert capsys.readouterr().err == string_to_log
        assert capsys.readouterr().out != string_to_log
    else:
        my_precious_logger(string_to_log)

        assert capsys.readouterr().out == string_to_log
        assert capsys.readouterr().err != string_to_log
