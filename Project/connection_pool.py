import os.path
import threading
import time
from queue import Empty, Queue, Full
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from os import getenv, environ
from dotenv import load_dotenv
import psycopg2

import sqlite3
from sqlite3 import Error


# zapytanie SQL ktre pokazuje liczbe otwartych polaczen aktualnych
# SELECT * FROM pg_stat_activity; -->> tylko postgresql

class ConnectionPool:
    def __init__(self, time_check=3, standard_amount_of_connections=10):
        # load_dotenv()
        self.db_params = None
        self.read_db_param()
        # self.database_uri = environ["DATABASE_URL"]
        self.time_check = time_check
        self.standard_amount_of_connections = standard_amount_of_connections
        self.max_connections = 90
        self.min_connections = 10
        self.active_connections = 0
        self.queue = Queue(maxsize=self.max_connections)
        self.semaphore = threading.Semaphore()
        self.init_connections()

    def read_db_param(self):
        self.db_params = os.path.abspath("/home/sebastian/GitHub/p206_l03_concurrency_SQLite/Project/sqlite.db")

    def init_connections(self):
        while self.queue.qsize() < self.min_connections:
            self.add_connection_to_queue(self.db_params)

    # start when serwer started
    def check_amount_of_conections(self):
        while True:
            if self.queue.qsize() > self.min_connections:
                for _ in range(self.queue.qsize() - self.min_connections):
                    conn = self.queue.get()
                    conn.close()
                    print("xxactive:", self.active_connections)
                    print("xxqueuesieze:", self.queue.qsize())
            print("CHECK_AMOUNT_OF_CONNECTIONS")
            time.sleep(40)

    def get_connection(self):
        with self.semaphore:
            conn = None
            try:
                conn = self.queue.get(block=False)
                self.active_connections += 1
            except Empty:
                if self.add_connection_to_queue(self.db_params):
                    conn = self.queue.get()
                    self.active_connections += 1
            print("active:", self.active_connections)
            print("queuesieze:", self.queue.qsize())
            return conn

    def add_connection_to_queue(self, param_db):
        if isinstance(param_db, str) and self.active_connections < self.max_connections:
            # add new connection
            print("string path")
            conn = None
            try:
                conn = sqlite3.connect(param_db, check_same_thread=False)
            except Error as e:
                print("Error SQL", e)
            self.queue.put(conn)
            return True
        elif isinstance(param_db, sqlite3.Connection) and self.queue.qsize() < self.max_connections:
            # add old connection
            print("puuuuuuttttttt")
            self.queue.put(param_db)
            return True
        else:
            raise TooMuchConnections

    def release_connection(self, conn):
        with self.semaphore:
            try:
                if conn is not None:
                    self.add_connection_to_queue(conn)
                    self.active_connections -= 1
                    print("Relactive:", self.active_connections)
                    print("Relqueuesieze:", self.queue.qsize())
            except:
                print("except release")
                pass


if __name__ == '__main__':
    conn = ConnectionPool()
    conn.init_connections()


class TooMuchConnections(Exception):
    pass
