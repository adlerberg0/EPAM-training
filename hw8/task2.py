"""
We have a database file (example.sqlite) in sqlite3 format with some tables and data.
All tables have 'name' column and maybe some additional ones.

Data retrieval and modifications are done with sqlite3 module by issuing SQL statements.
For example, to get all data from TABLE1:

import sqlite3
conn = sqlite3.connect('example.db')
cursor = conn.cursor()
cursor.execute('SELECT * from TABLE1')
data = cursor.fetchall()   # will be a list with data.
instead of getting all data at once, you can use .fetchone() calls and named expressions:

while row:=cursor.fetchone():
    print(row)
To get a row with specific name equal to some value:

import sqlite3
conn = sqlite3.connect('example.db')
cursor = conn.cursor()
cursor.execute('SELECT * from presidents where name=:name', {name:'Yeltsin'})
data = cursor.fetchall()  # will get all records with this name. You can also use .fetchone() to get one record.
in order to get record with first name (sorted alphabetically) use
    SQL expression SELECT * from presidents order by name asc limit 1
in order to get record after specified (sorted alphabetically) use
    SQL expression SELECT * from presidents where name > :name order by name limit.
To get amount of records in table TABLE1, use select count(*) from TABLE1 query.

Please refer to this documents for more information about how to retrieve data from sqlite database:
DB_API: https://www.python.org/dev/peps/pep-0249/
sqlite3 module: https://docs.python.org/3/library/sqlite3.html

Task
    Write a wrapper class TableData for database table,
that when initialized with database name and table acts as collection object (implements Collection protocol).
Assume all data has unique values in 'name' column.

So, if presidents = TableData(database_name='example.sqlite', table_name='presidents')
then len(presidents) will give current amount of rows in presidents table in database
    presidents['Yeltsin'] should return single data row for president with name Yeltsin.
    'Yeltsin' in presidents should return if president with same name exists in table

object implements iteration protocol. i.e. you could use it in for loops::
    for president in presidents:
        print(president['name'])
all above mentioned calls should reflect most recent data.
If data in table changed after you created collection self.instance, your calls should return updated data.

Avoid reading entire table into memory.
When iterating through records, start reading the first record, then go to the next one,
until records are exhausted.
When writing tests, it's not always necessary to mock database calls completely.
Use supplied example.sqlite file as database fixture file.
"""

from sqlite3 import Cursor, connect
from typing import Any, Iterable


class TableData:
    def __init__(self, db_path: str, table_name: str):
        self.db_path = db_path
        self.table_name = table_name

    @staticmethod
    def db_connection(func):
        def wrapper(self, *args, **kwargs):
            with connect(self.db_path) as db_connection:
                res = func(self, *args, db_cursor=db_connection.cursor(), **kwargs)
                db_connection.commit()
            return res

        return wrapper

    @db_connection.__func__
    def __getitem__(self, item: str, db_cursor: Cursor = None) -> tuple:
        db_cursor.execute(f"SELECT * from {self.table_name} where name==(?)", (item,))
        res = db_cursor.fetchone()
        if res is None:
            raise KeyError
        return res

    @db_connection.__func__
    def __setitem__(self, key: str, value: Any, db_cursor: Cursor = None) -> None:
        db_cursor.execute(f"REPLACE into {self.table_name} VALUES (?, ?, ?)", value)

    def __iter__(self, db_cursor: Cursor = None) -> Iterable:
        return self.__next__()

    @db_connection.__func__
    def __next__(self, db_cursor: Cursor = None) -> tuple:
        db_cursor.execute(f"SELECT * from {self.table_name}")

        while row := db_cursor.fetchone():
            yield row[0], row

    @db_connection.__func__
    def __len__(self, db_cursor: Cursor = None) -> int:
        db_cursor.execute(f"SELECT count(*) from {self.table_name}")

        return db_cursor.fetchone()[0]
