import pathlib

import pytest

from hw8.task2 import TableData

path_to_db = pathlib.Path.cwd().joinpath("tests", "hw8", "example.sqlite")


class TestClass:
    @classmethod
    def setup(cls):
        cls.instance = TableData(path_to_db, "Presidents")

    def test_retrieving_params(self):

        assert self.__class__.instance["Yeltsin"] == ("Yeltsin", 999, "Russia")

    def test_assign_params(self):

        self.__class__.instance["Big Man Tyrone"] = ("Big Man Tyrone", 54, "Kekistan")
        assert self.__class__.instance["Big Man Tyrone"] == (
            "Big Man Tyrone",
            54,
            "Kekistan",
        )

        self.__class__.instance["Big Man Tyrone"] = ("Big Man Tyrone", 101, "Kekistan")
        assert self.__class__.instance["Big Man Tyrone"] == (
            "Big Man Tyrone",
            101,
            "Kekistan",
        )

    def test_iterate_through_table_raws(self):
        tmp_data = {
            "Yeltsin": ("Yeltsin", 999, "Russia"),
            "Trump": ("Trump", 1337, "US"),
            "Big Man Tyrone": ("Big Man Tyrone", 101, "Kekistan"),
        }
        for president, personality in self.__class__.instance:
            assert president in tmp_data
            assert personality == tmp_data[president]
        # test second circle
        for president, personality in self.__class__.instance:
            assert president in tmp_data
            assert personality == tmp_data[president]

    def test_len_method_of_the_self(self):

        tmp_data = {
            "Yeltsin": ("Yeltsin", 999, "Russia"),
            "Trump": ("Trump", 1337, "US"),
            "Big Man Tyrone": ("Big Man Tyrone", 101, "Kekistan"),
        }
        assert len(self.__class__.instance) == len(tmp_data)

    def test_assigning_unexisting_value(self):

        with pytest.raises(KeyError):
            self.__class__.instance["Gurbanguly Berdimuhamedow"] == (
                "Gurbanguly Berdimuhamedow",
                63,
                "Turkmenistan",
            )
