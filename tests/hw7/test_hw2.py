from hw7.hw2 import backspace_compare


def test_backspace_compare_with_one_backspace():
    assert backspace_compare("ab#c", "ad#c")


def test_backspace_compare_with_multiple_backspace():
    assert backspace_compare("a##c", "##a#c")


def test_backspace_compare_with_first_backspace():
    assert backspace_compare("##ac", "ac")


def test_backspace_compare_negative_case():
    assert not backspace_compare("a#c", "b")
