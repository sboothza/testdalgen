from datetime import datetime

from src.base.session import Session
from src.base.repository_base import RepositoryBase
import entities.entities
import src.repositories.customer_region_repository
import src.repositories.order_repository


class CustomerRepository(RepositoryBase):
    __table__ = entities.entities.Customer
    order_repo: src.repositories.order_repository.OrderRepository
    customer_region_repo: src.repositories.customer_region_repository.CustomerRegionRepository

    def __init__(self, order_repo: src.repositories.order_repository.OrderRepository,
                 customer_region_repo: src.repositories.customer_region_repository.CustomerRegionRepository):
        self.order_repo = order_repo
        self.customer_region_repo = customer_region_repo

    def get_by_id(self, session: Session, id: int):
        item: entities.entities.Customer = self._get_by_id(session, {"id": id})
        item.orders = self.order_repo.get_for_customer(session, item.id)
        item.regions = self.customer_region_repo.get_regions(item)
        return item

    def exists(self, session: Session, id: int):
        return self._item_exists(session, {"id": id})

    def delete(self, session: Session, id: int):
        item = self.get_by_id(id)
        for order in item.orders:
            self.order_repo.delete(order.id)

        for region in item.regions:
            self.customer_region_repo.delete(session, {"customerid": item.id, "regionid": region.id})

        self._delete(session, {"id": id})

    def add(self, session: Session, item: entities.entities.Customer):
        id = self._execute_lastrowid(session, item.__insert_script__, item.get_insert_params())
        item.id = id
        for order in item.orders:
            order.customer_id = id
            self.order_repo.add(session, order)

        for region in item.regions:
            customer_region = entities.entities.CustomerRegion(item.id, region.id)
            self.customer_region_repo.add(session, customer_region)

    # end-autogenerated

    def get_by_name(self, session: Session, name: str):
        row = self._fetch_one(session, "select \"id\", \"name\", \"email\", \"enabled\" from \"customer\" where "
                                       "\"name\" = :name;", {"name": name})
        if not row:
            return None

        item: entities.entities.Customer = self.__table__().map_row(row)

        item.order = self.order_repo.get_for_customer(session, item.id)
        item.regions = self.customer_region_repo.get_regions(item)
        return item