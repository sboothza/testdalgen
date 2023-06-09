from src.base.exceptions import DataException
from src.base.session import Session
from src.base.repository_base import RepositoryBase
import entities.entities


class CustomerRegionRepository(RepositoryBase):
    __table__ = entities.entities.CustomerRegion

    def __init__(self):
        ...

    def get_by_id(self, session: Session, id: None):
        if id is None:
            raise DataException("id cannot be null")

        item: entities.entities.CustomerRegion = self._get_by_id(session, id)
        return item

    def exists(self, session: Session, id: None):
        if id is None:
            raise DataException("id cannot be null")

        return self._item_exists(session, id)

    def delete(self, session: Session, id: None):
        if id is None:
            raise DataException("id cannot be null")

        self._delete(session, id)

    def add(self, session: Session, item: entities.entities.CustomerRegion):
        self._execute(session, item.__insert_script__, item.get_insert_params())

    def get_regions(self, session: Session, item: entities.entities.Customer):
        with session.fetch("select id, name from region inner join customerregion on region.id = customerregion."
                           "regionid where customerregion.customerid = :customerid", {"customerid": item.id}) as cursor:
            return [entities.entities.Region.__table__().map_row(row) for row in cursor]

    def get_customers(self, session: Session, item: entities.entities.Region):
        with session.fetch("select id, name email, enabled from customer inner join customerregion on customer.id = "
                           "customerregion.customerid where customerregion.regionid = :regionid",
                           {"regionid": item.id}) as cursor:
            return [entities.entities.Customer.__table__().map_row(row) for row in cursor]

# end-autogenerated
