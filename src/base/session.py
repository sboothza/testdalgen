import re

from src.base.connection_base import ConnectionBase, SqliteConnection, MySqlConnection
from src.base.managed_cursor import ManagedCursor


class Session(object):
    def __init__(self, connection: ConnectionBase = None):
        self.connection = connection

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self.connection.commit()
        self.connection.close()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def execute(self, query: str, params=None) -> None:
        if params is None:
            params = {}
        self.connection.execute(query, params)

    def fetch_scalar(self, query: str, params=None):
        if params is None:
            params = {}
        row = self.fetch_one(query, params)
        if row is not None:
            value = row[0]
        else:
            value = None
        return value

    def fetch_one(self, query: str, params=None):
        if params is None:
            params = {}
        with self.connection.execute(query, params) as cursor:
            return cursor.fetchone()

    def fetch(self, query: str, params=None) -> ManagedCursor:
        if params is None:
            params = {}
        return self.connection.execute(query, params)


class PersistentSession(Session):
    __global_connection__: ConnectionBase = None

    def __init__(self, connection: ConnectionBase = None):
        if PersistentSession.__global_connection__ is None:
            PersistentSession.__global_connection__ = connection

        self.connection = PersistentSession.__global_connection__

    def __exit__(self, type, value, traceback):
        self.connection.commit()

    def close(self):
        pass


class SessionFactory(object):
    @staticmethod
    def get_connection(connection_string: str) -> ConnectionBase:
        match = re.search(r"(\w+):\/\/(.+)", connection_string)
        if match:
            db_type = match.group(1)

            if db_type == "sqlite":
                return SqliteConnection(connection_string)
            elif db_type == "mysql":
                return MySqlConnection(connection_string)

    @staticmethod
    def connect(connection_string: str) -> Session:
        if "memory" in connection_string:
            if PersistentSession.__global_connection__ is None:
                session = PersistentSession(SessionFactory.get_connection(connection_string))
            else:
                session = PersistentSession()

        else:
            session = Session(SessionFactory.get_connection(connection_string))

        return session
