from entities.order_status import OrderStatus
from src.base.session import Session
from src.base.repository_base import RepositoryBase


class OrderStatusRepository(RepositoryBase):
    __table__ = OrderStatus

    def __init__(self):
        ...

    def get_by_id(self, session: Session, id: int):
        item: OrderStatus = self._get_by_id(session, {"id": id})
        return item

    def exists(self, session: Session, id: int):
        return self._item_exists(session, {"id": id})

    def delete(self, session: Session, id: int):
        self._delete(session, {"id": id})

    def add(self, session: Session, item: OrderStatus):
        id = session.execute_lastrowid(item.__insert_script__, item.get_insert_params())
        item.id = id

    # end-autogenerated
    def get_by_name(self, session: Session, name: str):
        row = OrderStatus.fetch_one(session,
                                    """
                                    select "id", "value" from "orderstatus" 
                                    where "value" = %(name)s;
                                    """, {"name": name})
        if not row:
            return None

        item: OrderStatus = OrderStatus.map_row(row)
        return item
