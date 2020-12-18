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
from typing import Union


class KeyValueStorage:
    def __init__(self, file_path: str):
        super().__setattr__("_file_path", file_path)

        if not path.isfile(file_path):
            raise FileNotFoundError
        with open(file_path) as f:
            # use specified dict to prevent rewriting collisions of class attributes from __dict__
            super().__setattr__("_file_content", {})
            for line in f:
                key, value = line.strip().split("=")
                if value.isdigit():
                    value = int(value)
                self._file_content[key] = value

    def __getattr__(self, item: str) -> Union[int, str]:
        """
        Get attribute value through . notation
        """
        try:
            res = self._file_content[item]
        except KeyError:
            raise AttributeError
        return res

    def __getitem__(self, item: str) -> Union[int, str]:
        """
        Get attribute value via square brackets
        """
        if item in self.__dict__:
            return self.item

        return self._file_content[item]

    def __setattr__(self, name: str, value: Union[int, str]) -> None:
        """
        Set attribute value through . notation
        """
        if name in self.__dict__:
            super().__setattr__(name, value)
            return
        # a value type check
        if not isinstance(value, (int, str)):
            raise ValueError

        self.change_or_delete_line_from_file(self._file_path, name, value)
        self._file_content[name] = value

    def __setitem__(self, key: str, value: Union[int, str]) -> None:
        """
        Set attribute value via square brackets
        """
        # a value type check
        if not isinstance(value, (int, str)):
            raise ValueError

        self.change_or_delete_line_from_file(self._file_path, key, value)
        self._file_content[key] = value

    def __delitem__(self, key: str) -> None:
        """
        Delete item from _file_storage and file
        """
        if key not in self._file_content:
            raise KeyError

        self.change_or_delete_line_from_file(self._file_path, key, None, delete=True)
        self._file_content.pop(key)

    @staticmethod
    def change_or_delete_line_from_file(
        filepath: str,
        key: str,
        value: Union[int, str, None] = None,
        delete: bool = False,
    ) -> None:
        if not path.isfile(filepath):
            raise FileNotFoundError

        result_file_str = ""
        is_found = False
        with open(filepath, mode="r+") as f:
            for line in f:
                if line == "":
                    continue
                file_key, old_value = line.strip().split("=")
                if file_key == key:
                    is_found = True
                    if delete:
                        continue
                    result_file_str += f"{file_key}={value}\n"
                else:
                    result_file_str += f"{file_key}={old_value}\n"

            if not is_found and not delete:
                result_file_str += f"{key}={value}\n"
            f.seek(0, 0)
            f.write(result_file_str)
