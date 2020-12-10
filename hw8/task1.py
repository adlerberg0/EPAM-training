"""
We have a file that works as key-value storage, each like is represented as key and value separated by = symbol, example:

name=kek last_name=top song_name=shadilay power=9001

Values can be strings or integer numbers. If a value can be treated both as a number and a string,
 it is treated as number.

Write a wrapper class for this key value storage that works like this:

storage = KeyValueStorage('path_to_file.txt')
that has its keys and values accessible as collection items and as attributes.
Example:
    storage['name'] # will be string 'kek'
    storage.song_name # will be 'shadilay'
    storage.power # will be integer 9001

In case of attribute clash existing built-in attributes take precedence.
In case when value cannot be assigned to an attribute (for example when there's a line 1=something)
 ValueError should be raised.
 File size is expected to be small, you are permitted to read it entirely into memory.
"""
from os import path
from typing import Any


def change_or_delete_line_from_file(
    filepath: str, key: str, value: Any, delete: bool = False
):
    if not path.isfile(filepath):
        raise ValueError

    result_file_str = ""
    with open(filepath, mode="r") as f:
        for line in f:
            file_key, old_value = line.strip().split("=")
            if file_key == key:
                if delete:
                    continue
                result_file_str += f"{file_key}={value}\n"
            else:
                result_file_str += f"{file_key}={old_value}\n"
    with open(filepath, mode="w") as f:
        f.write(result_file_str)


class KeyValueStorage:
    def __init__(self, file_path: str):
        super().__setattr__(
            "_file_path", file_path
        )  # or self.__dict__["_file_path"] = file_path
        if not path.isfile(file_path):
            raise ValueError
        with open(file_path) as f:
            # use specified dict to prevent rewriting collisions of class attributes from __dict__
            super().__setattr__("_file_storage", {})
            for line in f:
                key, value = line.strip().split("=")
                if value.isdigit():
                    value = int(value)
                super().__getattribute__("_file_storage")[key] = value

    def __getattribute__(self, item: str):
        """
        Get attribute value through . notation
        """
        # try access to inner attributes and methods through . notation
        try:
            inner_data = super().__getattribute__(item)
        except AttributeError:
            ...  # do nothing
        else:
            return inner_data
        # or obtain item from file storage
        return super().__getattribute__("_file_storage").get(item)

    def __getitem__(self, item: str) -> Any:
        """
        Get attribute value via square brackets
        """
        try:
            res = super().__getattribute__("_file_storage").get(item)
        except AttributeError:
            self.__missing__(item)
        return res

    def __setattr__(self, name: str, value: Any):
        """
        Set attribute value through . notation
        """
        # a name presence and a value type check
        file_path = super().__getattribute__("_file_path")
        file_storage = super().__getattribute__("_file_storage")
        if name not in file_storage:
            raise AttributeError
        if not isinstance(value, type(file_storage[name])):
            raise ValueError

        change_or_delete_line_from_file(file_path, name, value)
        file_storage[name] = value

    def __setitem__(self, key, value):
        """
        Set attribute value via square brackets
        """
        # a name presence and a value type check
        file_path = super().__getattribute__("_file_path")
        file_storage = super().__getattribute__("_file_storage")
        if key not in file_storage:
            raise AttributeError
        if not isinstance(value, type(file_storage[key])):
            raise ValueError

        change_or_delete_line_from_file(file_path, key, value)
        file_storage[key] = value

    def __delitem__(self, key: str):
        """
        Delete item from _file_storage and file
        """
        file_path = super().__getattribute__("_file_path")
        file_storage = super().__getattribute__("_file_storage")
        if key not in file_storage:
            raise AttributeError

        change_or_delete_line_from_file(file_path, key, None, delete=True)
        file_storage.pop(key)

    def __getattr__(self, item: str):
        """
        Is called by __getattribute__ when AttributeError is risen
        """
        raise AttributeError

    def __missing__(self, key: str):
        """
        Is called by __getitem__ when AttributeError is risen
        """
        print(f"There is no {key}")
        raise AttributeError

    def _get_copy_of_storage_dict(self) -> dict:
        """
        Helping method for tests
        """
        return super().__getattribute__("_file_storage").copy()


# why do we have recursion with self.__dict__[item]??
