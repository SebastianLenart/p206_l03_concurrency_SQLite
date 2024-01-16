import os
from dotenv import load_dotenv
from psycopg2.pool import SimpleConnectionPool
from configparser import ConfigParser
from contextlib import contextmanager


class GetConnection:
    def __init__(self):
        load_dotenv()
        self.database_uri = os.environ["DATABASE_URL"]
        # self.params = self.config()
        # self.pool = SimpleConnectionPool(minconn=1, maxconn=10, **self.params)
        self.pool = SimpleConnectionPool(minconn=1, maxconn=10, dsn=self.database_uri)
        self.connection = None

    def __enter__(self):
        # print("enter")
        self.connection = self.pool.getconn()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # print("exit")
        if isinstance(exc_type, Exception):
            self.connection.rollback()
        self.pool.putconn(self.connection)

    def config(self, filename='database.ini', section='postgresql'):
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(filename)

        # get section, default to postgresql
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))
        print("****************")
        return db

    @contextmanager
    def get_cursor(self):
        with self.connection:  # z tym dziala
            with self.connection.cursor() as cursor:
                yield cursor




