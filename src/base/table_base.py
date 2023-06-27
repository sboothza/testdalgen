from datetime import datetime
import time
from typing import Union

from base.session import Session


class TableBase:
    pass


class TableBase:
    __table_name__ = ""
    __table_exists_script__ = ""
    __table_count_script__ = ""
    __drop_script__ = ""
    __create_script__ = ""
    __insert_script__ = ""
    __update_script__ = ""
    __delete_script__ = ""
    __fetch_by_id_script__ = ""
    __item_exists_script__ = ""

    @classmethod
    def map_row(cls, row) -> TableBase:
        pass

    def get_insert_params(self) -> {}:
        pass

    def get_update_params(self) -> {}:
        pass

    @classmethod
    def fetch_one(cls, session: Session, query: str, parameters=None) -> Union[TableBase, TableBase, None]:
        if parameters is None:
            parameters = {}
        row = session.fetch_one(query, parameters)
        if row:
            return cls.map_row(row)
        return None

    @classmethod
    def fetch(cls, session: Session, query: str, parameters=None):
        if parameters is None:
            parameters = {}
        with session.fetch(query, parameters) as cursor:
            return [cls.map_row(row) for row in cursor]

    @staticmethod
    def int_to_bool(value: int) -> bool:
        return value != 0

    @staticmethod
    def bool_to_int(value: bool) -> int:
        return 1 if value else 0

    @staticmethod
    def float_to_datetime(value: float) -> datetime:
        return datetime.fromtimestamp(value)

    @staticmethod
    def datetime_to_float(value: datetime) -> float:
        return time.mktime(value.timetuple())
