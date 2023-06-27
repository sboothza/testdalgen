from typing import Union

from src.base.exceptions import DataException
from src.base.session import Session
from src.base.table_base import TableBase


class RepositoryBase:
    __table__ = TableBase

    def drop_schema(self, session: Session):
        session.execute(self.__table__.__drop_script__)

    def schema_exists(self, session: Session):
        script = self.__table__.__table_exists_script__.format(database=session.connection.database)
        name = session.fetch_scalar(script)
        if name != self.__table__.__table_name__:
            return False

        return True

    def create_schema(self, session: Session):
        script = list(filter(None, self.__table__.__create_script__.split(";")))
        for line in script:
            session.execute(line + ";")

    def _get_by_id(self, session: Session, id: {}):
        if id is None:
            raise DataException("id cannot be null")
        row = session.fetch_one(self.__table__.__fetch_by_id_script__, id)
        if row:
            return self.__table__().map_row(row)
        return None

    def _item_exists(self, session: Session, id: {}):
        if id is None:
            raise DataException("id cannot be null")
        cnt = session.fetch_scalar(self.__table__.__item_exists_script__, id)
        return cnt > 0

    def count(self, session: Session):
        script = self.__table__.__table_count_script__
        return session.fetch_scalar(script)

    def add(self, session: Session, item: TableBase):
        pass

    def update(self, session: Session, item: TableBase):
        session.execute(self.__table__.__update_script__, item.get_update_params())

    def _delete(self, session: Session, id: {}):
        if id is None:
            raise DataException("id cannot be null")
        session.execute(self.__table__.__delete_script__, id)
