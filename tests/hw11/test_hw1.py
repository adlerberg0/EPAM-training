from hw11.hw1 import SimplifiedEnum


def test_simplified_enum_usage():
    class ColorsEnum(metaclass=SimplifiedEnum):
        __keys = ("RED", "BLUE", "ORANGE", "BLACK")

    class SizesEnum(metaclass=SimplifiedEnum):
        __keys = ("XL", "L", "M", "S", "XS")

    assert ColorsEnum.RED == "RED"
    assert SizesEnum.XL == "XL"


def test_traversing_through_enum():
    colours = ("RED", "BLUE", "ORANGE", "BLACK")

    class ColorsEnum(metaclass=SimplifiedEnum):
        __keys = colours

    for i, value in enumerate(ColorsEnum):
        assert value == colours[i]
