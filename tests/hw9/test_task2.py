import pytest

from hw9.task2 import SupressorClass, supressor_gen


class TestClass:
    def test_gen_exception_supression(self):
        with supressor_gen(IndexError):
            raise IndexError

    def test_gen_do_not_supress_another_exception(self):
        with pytest.raises(BaseException):
            with supressor_gen(IndexError):
                raise BaseException

    def test_class_exception_supression(self):
        with SupressorClass(IndexError):
            raise IndexError

    def test_class_do_not_supress_another_exception(self):
        with pytest.raises(BaseException):
            with SupressorClass(IndexError):
                raise BaseException
