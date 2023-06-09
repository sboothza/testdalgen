# from typing import List
# # import entities.order
# # import entities.region
# from base.table_base import TableBase
# from entities.order import *
# from entities.region import *
#
#
# class Customer(TableBase):
#     __table_name__ = "customer"
#     __drop_script__ = "None"
#     __create_script__ = "create table \"customer\" (\"id\" INTEGER ,\"name\" TEXT ,\"email\" TEXT ,\"enabled\" INTEGER ,PRIMARY KEY (\"id\")); CREATE INDEX \"customer_name_IDX\" ON \"customer\" (\"name\");"
#     __table_exists_script__ = "SELECT name FROM sqlite_schema WHERE type='table' and name = 'customer'"
#     __table_count_script__ = "select count(*) from \"customer\""
#     __insert_script__ = "insert into \"customer\" (\"name\", \"email\", \"enabled\") values (:name, :email, :enabled);"
#     __update_script__ = "update \"customer\" set \"name\" = :name, \"email\" = :email, \"enabled\" = :enabled where \"id\" = :id;"
#     __delete_script__ = "delete from \"customer\" where \"id\" = :id;"
#     __fetch_by_id_script__ = "select \"id\", \"name\", \"email\", \"enabled\" from \"customer\" where \"id\" = :id;"
#     __item_exists_script__ = "select count(*) from \"customer\" where \"id\" = :id;"
#
#     id: int = 0
#     name: str = "None"
#     email: str = "None"
#     enabled: bool = True
#
#     orders: List[Order]  # order_FK_1
#     regions: List[Region]
#
#     def __init__(self, id: int = 0, name: str = "", email: str = "None", enabled: bool = True):
#         self.id = id
#         self.name = name
#         self.email = email
#         self.enabled = enabled
#         self.orders: List[entities.order.Order] = list()
#         self.regions: List[entities.region.Region] = list()
#
#     def map_row(self, row) -> TableBase:
#         self.id = row[0]
#         self.name = row[1]
#         self.email = row[2]
#         self.enabled = TableBase.int_to_bool(row[3])
#         return self
#
#     def get_insert_params(self) -> {}:
#         return {"name": self.name, "email": self.email, "enabled": TableBase.bool_to_int(self.enabled)}
#
#     def get_update_params(self) -> {}:
#         return {"name": self.name, "email": self.email, "enabled": TableBase.bool_to_int(self.enabled), "id": self.id}
#
# # end-autogenerated
