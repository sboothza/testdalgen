# from src.base.table_base import TableBase
#
#
# class OrderLine(TableBase):
#     __table_name__ = "orderline"
#     __drop_script__ = "None"
#     __create_script__ = "create table \"orderline\" (\"id\" INTEGER ,\"orderid\" INTEGER ,\"productid\" INTEGER ,\"quantity\" REAL ,\"price\" REAL ,PRIMARY KEY (\"id\"),FOREIGN KEY (\"orderid\") REFERENCES \"order\"(\"id\"),FOREIGN KEY (\"productid\") REFERENCES \"product\"(\"id\")); CREATE INDEX \"orderline_FK\" ON \"orderline\" (\"orderid\"); CREATE INDEX \"orderline_FK_1\" ON \"orderline\" (\"productid\");"
#     __table_exists_script__ = "SELECT name FROM sqlite_schema WHERE type='table' and name = 'orderline'"
#     __table_count_script__ = "select count(*) from \"orderline\""
#     __insert_script__ = "insert into \"orderline\" (\"orderid\", \"productid\", \"quantity\", \"price\") values (:orderid, :productid, :quantity, :price);"
#     __update_script__ = "update \"orderline\" set \"orderid\" = :orderid, \"productid\" = :productid, \"quantity\" = :quantity, \"price\" = :price where \"id\" = :id;"
#     __delete_script__ = "delete from \"orderline\" where \"id\" = :id;"
#     __fetch_by_id_script__ = "select \"id\", \"orderid\", \"productid\", \"quantity\", \"price\" from \"orderline\" where \"id\" = :id;"
#     __item_exists_script__ = "select count(*) from \"orderline\" where \"id\" = :id;"
#
#     id: int = 0
#     order_id: int = 0
#     product_id: int = 0
#     quantity: float = 0
#     price: float = 0
#
#     def __init__(self, id: int = 0, order_id: int = 0, product_id: int = 0, quantity: float = 0, price: float = 0):
#         self.id = id
#         self.order_id = order_id
#         self.product_id = product_id
#         self.quantity = quantity
#         self.price = price
#
#     def map_row(self, row) -> TableBase:
#         self.id = row[0]
#         self.order_id = row[1]
#         self.product_id = row[2]
#         self.quantity = row[3]
#         self.price = row[4]
#         return self
#
#     def get_insert_params(self) -> {}:
#         return {"orderid": self.order_id, "productid": self.product_id, "quantity": self.quantity, "price": self.price}
#
#     def get_update_params(self) -> {}:
#         return {"orderid": self.order_id, "productid": self.product_id, "quantity": self.quantity, "price": self.price,
#                 "id": self.id}
#
# # end-autogenerated
