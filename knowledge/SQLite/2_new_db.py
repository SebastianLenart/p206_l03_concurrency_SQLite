"""
If you skip the folder path c:\sqlite\db, the program will create the database file in the current working directory (CWD).

If you pass the file name as :memory: to the connect() function of the sqlite3 module, it will create a new database that resides in the memory (RAM) instead of a database file on disk.

The following program creates an SQLite database in the memory.


"""

import sqlite3
from sqlite3 import Error


def create_connection():
    """ create a database connection to a database that resides
        in the memory
    """
    conn = None;
    try:
        conn = sqlite3.connect(':memory:')
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    create_connection()