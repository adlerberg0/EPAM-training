import pytest

from hw8.task1 import KeyValueStorage


@pytest.fixture(scope="module")
def key_value_storage_instance():
    instance = KeyValueStorage("task1.txt")
    storage = instance._get_copy_of_storage_dict()
    yield instance
    for key, value in storage.items():
        instance[key] = value


def test_reading_char_and_integer_value_from_file(key_value_storage_instance):
    instance = key_value_storage_instance

    assert instance["name"] == "Shale"
    assert instance["Strength"] == 18


def test_assigning_char_and_int_value_to_storage(key_value_storage_instance):
    instance = key_value_storage_instance

    instance.Spec = "Pulverizing Blows"
    instance.Strength = 21

    assert instance.Spec == "Pulverizing Blows"
    assert instance.Strength == 21


def test_assigning_char_and_int_value_to_storage_via_square_bracket(
    key_value_storage_instance,
):
    instance = key_value_storage_instance

    instance["Spec"] = "Rock Mastery"
    instance["Constitution"] = 15

    assert instance["Spec"] == "Rock Mastery"
    assert instance["Constitution"] == 15


def test_assigning_wrong_value_to_storage(key_value_storage_instance):
    instance = key_value_storage_instance

    with pytest.raises(ValueError):
        instance["Constitution"] = "18"
    with pytest.raises(ValueError):
        instance["last_name"] = 0
    with pytest.raises(AttributeError):
        instance[
            "unexisting_attribute_with_quotes"
        ] = "I wonder what it is like to float...or drown."


def test_assigning_wrong_value_or_attribute_to_storage(key_value_storage_instance):
    instance = key_value_storage_instance

    with pytest.raises(ValueError):
        instance.Constitution = "18"
    with pytest.raises(ValueError):
        instance.last_name = 0

    with pytest.raises(ValueError):
        instance["Constitution"] = "18"
    with pytest.raises(ValueError):
        instance["last_name"] = 0

    with pytest.raises(AttributeError):
        instance.unexisting_attribute_with_quotes = (
            "I wonder what it is like to float...or drown."
        )
