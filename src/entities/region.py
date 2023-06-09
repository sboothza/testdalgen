# from typing import List
# import entities.customer
# from src.base.table_base import TableBase
#
#
# class Region(TableBase):
#     __table_name__ = "region"
#     __drop_script__ = "None"
#     __create_script__ = "create table \"region\" (\"id\" INTEGER ,\"name\" TEXT ,PRIMARY KEY (\"id\")); CREATE INDEX \"region_name_IDX\" ON \"region\" (\"name\");"
#     __table_exists_script__ = "SELECT name FROM sqlite_schema WHERE type='table' and name = 'region'"
#     __table_count_script__ = "select count(*) from \"region\""
#     __insert_script__ = "insert into \"region\" (\"id\", \"name\") values (:name);"
#     __update_script__ = "update \"region\" set \"name\" = :name where \"id\" = :id;"
#     __delete_script__ = "delete from \"region\" where \"id\" = :id;"
#     __fetch_by_id_script__ = "select \"id\", \"name\" from \"region\" where \"id\" = :id;"
#     __item_exists_script__ = "select count(*) from \"region\" where \"id\" = :id;"
#
#     id: int = 0
#     name: str = ""
#     customers: List[entities.customer.Customer]
#
#     def __init__(self, id: int = 0, name: str = ""):
#         self.id = id
#         self.name = name
#         self.customers: List[entities.customer.Customer] = list()
#
#     def map_row(self, row) -> TableBase:
#         self.id = row[0]
#         self.name = row[1]
#         return self
#
#     def get_insert_params(self) -> {}:
#         return {"name": self.name}
#
#     def get_update_params(self) -> {}:
#         return {"name": self.name, "id": self.id}
#
# # end-autogenerated
