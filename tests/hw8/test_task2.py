import pytest

from hw8.task2 import TableData


@pytest.fixture(scope="module")
def table_data_instance():
    yield TableData("example.sqlite")


def test_retrieving_params(table_data_instance):
    instance = table_data_instance

    assert instance["Yeltsin"] == ("Yeltsin", 999, "Russia")


def test_assign_params(table_data_instance):
    instance = table_data_instance

    instance["Big Man Tyrone"] = ("Big Man Tyrone", 54, "Kekistan")
    assert instance["Big Man Tyrone"] == ("Big Man Tyrone", 54, "Kekistan")

    instance["Big Man Tyrone"] = ("Big Man Tyrone", 101, "Kekistan")
    assert instance["Big Man Tyrone"] == ("Big Man Tyrone", 101, "Kekistan")


def test_iterate_through_table_raws(table_data_instance):
    instance = table_data_instance
    tmp_data = {
        "Yeltsin": ("Yeltsin", 999, "Russia"),
        "Trump": ("Trump", 1337, "US"),
        "Big Man Tyrone": ("Big Man Tyrone", 101, "Kekistan"),
    }
    for president, personality in instance:
        assert president in tmp_data
        assert personality == tmp_data[president]


def test_len_method_of_the_instance(table_data_instance):
    instance = table_data_instance
    tmp_data = {
        "Yeltsin": ("Yeltsin", 999, "Russia"),
        "Trump": ("Trump", 1337, "US"),
        "Big Man Tyrone": ("Big Man Tyrone", 101, "Kekistan"),
    }
    assert len(instance) == len(tmp_data)
