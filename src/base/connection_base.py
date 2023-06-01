import re
import sqlite3

import mysql.connector

from src.base.managed_cursor import ManagedCursor
from src.base.utils import get_filename, get_fullname


class ConnectionBase(object):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.database = ""

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def commit(self):
        pass

    def rollback(self):
        pass

    def execute(self, query: str, params: {}) -> ManagedCursor:
        pass

    def close(self):
        pass


class SqliteConnection(ConnectionBase):
    def __init__(self, connection_string):
        super().__init__(connection_string)
        connection_string = self.connection_string.replace("sqlite://", "")
        connection_string = get_fullname(connection_string)
        self.connection = sqlite3.connect(connection_string)
        self.database = get_filename(connection_string)

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def execute(self, query: str, params: None) -> ManagedCursor:
        if params is None:
            params = {}
        cursor = self.connection.execute(query, params)
        return ManagedCursor(cursor)

    def close(self):
        self.connection.close()


class MySqlConnection(ConnectionBase):
    def __init__(self, connection_string):
        super().__init__(connection_string)
        match = re.match(r"mysql:\/\/(\w+):(\w+)@(\w+)\/(\w+)", self.connection_string)
        if match:
            self.user = match.group(1)
            self.password = match.group(2)
            self.hostname = match.group(3)
            self.database = match.group(4)
        else:
            raise Exception("Invalid connection string")

        self.connection = mysql.connector.connect(user=self.user, password=self.password, host=self.hostname,
                                                  database=self.database)

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def execute(self, query: str, params: None) -> ManagedCursor:
        if params is None:
            params = {}
        cursor = self.connection.cursor(buffered=True)
        cursor.execute(query, params)
        return ManagedCursor(cursor)

    def close(self):
        self.commit()
        self.connection.close()
