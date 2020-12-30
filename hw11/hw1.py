"""
Vasya implemented nonoptimal Enum classes.
Remove duplications in variables declarations using metaclasses.
from enum import Enum
class ColorsEnum(Enum):
    RED = "RED"
    BLUE = "BLUE"
    ORANGE = "ORANGE"
    BLACK = "BLACK"
class SizesEnum(Enum):
    XL = "XL"
    L = "L"
    M = "M"
    S = "S"
    XS = "XS"
Should become:
class ColorsEnum(metaclass=SimplifiedEnum):
    __keys = ("RED", "BLUE", "ORANGE", "BLACK")
class SizesEnum(metaclass=SimplifiedEnum):
    __keys = ("XL", "L", "M", "S", "XS")
assert ColorsEnum.RED == "RED"
assert SizesEnum.XL == "XL"
"""
from typing import Iterable


class SimplifiedEnum(type):
    def __new__(mcs, name, bases, dct):
        dct["_dict_storage"] = {key: key for key in dct[f"_{name}__keys"]}
        cls_instance = super().__new__(mcs, name, bases, dct)

        return cls_instance

    def __getattr__(self, item):
        if item not in self._dict_storage:
            raise KeyError
        return self._dict_storage[item]

    def __iter__(self) -> Iterable:
        return self.__next__()

    def __next__(self) -> str:
        for value in self._dict_storage.values():
            yield value
