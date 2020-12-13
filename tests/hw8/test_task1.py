import pytest

from hw8.task1 import KeyValueStorage


class TestClass:
    @classmethod
    def setup_class(cls):
        cls.instance = KeyValueStorage("task1.txt")
        cls.storage = cls.instance._file_content.copy()

    @classmethod
    def teardown_class(cls):
        open("task1.txt", "w").close()
        for key, value in cls.storage.items():
            cls.instance[key] = value

    def test_reading_char_and_integer_value_from_file(self):

        assert self.__class__.instance["name"] == "Shale"
        assert self.__class__.instance["Strength"] == 18

    def test_assigning_char_and_int_value_to_storage(self):

        self.__class__.instance.Spec = "Pulverizing Blows"
        self.__class__.instance.Strength = 21

        assert self.__class__.instance.Spec == "Pulverizing Blows"
        assert self.__class__.instance.Strength == 21

    def test_assigning_char_and_int_value_to_storage_via_square_bracket(self):

        self.__class__.instance["Spec"] = "Rock Mastery"
        self.__class__.instance["Constitution"] = 15

        assert self.__class__.instance["Spec"] == "Rock Mastery"
        assert self.__class__.instance["Constitution"] == 15

    def test_assigning_wrong_value_to_storage(self):

        with pytest.raises(ValueError):
            self.__class__.instance["Constitution"] = 18.1
        with pytest.raises(ValueError):
            self.__class__.instance["last_name"] = ("A",)
        with pytest.raises(ValueError):
            self.__class__.instance.Constitution = 18.1
        with pytest.raises(ValueError):
            self.__class__.instance.last_name = ("A",)
        with pytest.raises(KeyError):
            self.__class__.instance["hates_pigeons"]

    def test_assigning_unexisting_key_or_attribute(self):

        self.__class__.instance.unexisting_attribute_with_quote1 = (
            "I wonder what it is like to float...or drown."
        )
        self.__class__.instance["unexisting_attribute_with_quote2"] = "Oooh, Shiny!"

        assert (
            self.__class__.instance.unexisting_attribute_with_quote1
            == "I wonder what it is like to float...or drown."
        )
        assert (
            self.__class__.instance.unexisting_attribute_with_quote2 == "Oooh, Shiny!"
        )

    def test_delete_value_from_the_storage(self):

        del self.__class__.instance["Willpower"]

        with pytest.raises(KeyError):
            self.__class__.instance["Willpower"]
