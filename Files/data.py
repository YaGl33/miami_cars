import sqlite3

sqlite_path = 'data/db.sqlite'


def get_all_values(table_name, column_name):
    connection = sqlite3.connect(sqlite_path)
    cursor = connection.cursor()
    result = cursor.execute(
        f"SELECT {column_name} FROM {table_name}"
    )
    answer = result.fetchall()
    return answer


def insert_values(table_name, value, column_name):
    connection = sqlite3.connect(sqlite_path)
    cursor = connection.cursor()
    cursor.execute(
        f"INSERT INTO {table_name} ({column_name}) VALUES('{value}')"
    )
    connection.commit()


def insert_many_values(table_name, values: list):
    connection = sqlite3.connect(sqlite_path)
    cursor = connection.cursor()
    cursor.executemany(
        f"INSERT INTO {table_name} VALUES(?, ?)",
        values
    )
    connection.commit()


def del_values(table_name, value, column_name):
    connection = sqlite3.connect(sqlite_path)
    cursor = connection.cursor()
    cursor.execute(
        f"DELETE FROM {table_name} WHERE {column_name}='{value}'"
    )
    connection.commit()