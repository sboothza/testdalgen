from datetime import datetime
from typing import List

from base.table_base import TableBase


class Customer(TableBase):
    ...


class CustomerRegion(TableBase):
    ...


class Order(TableBase):
    ...


class OrderLine(TableBase):
    ...


class OrderStatus(TableBase):
    ...


class Product(TableBase):
    ...


class Region(TableBase):
    ...


class Customer(TableBase):
    __table_name__ = "customer"
    __drop_script__ = "None"
    __create_script__ = "create table \"customer\" (\"id\" INTEGER ,\"name\" TEXT ,\"email\" TEXT ,\"enabled\" INTEGER ,PRIMARY KEY (\"id\")); CREATE INDEX \"customer_name_IDX\" ON \"customer\" (\"name\");"
    __table_exists_script__ = "SELECT name FROM sqlite_schema WHERE type='table' and name = 'customer'"
    __table_count_script__ = "select count(*) from \"customer\""
    __insert_script__ = "insert into \"customer\" (\"name\", \"email\", \"enabled\") values (:name, :email, :enabled);"
    __update_script__ = "update \"customer\" set \"name\" = :name, \"email\" = :email, \"enabled\" = :enabled where \"id\" = :id;"
    __delete_script__ = "delete from \"customer\" where \"id\" = :id;"
    __fetch_by_id_script__ = "select \"id\", \"name\", \"email\", \"enabled\" from \"customer\" where \"id\" = :id;"
    __item_exists_script__ = "select count(*) from \"customer\" where \"id\" = :id;"

    id: int = 0
    name: str = "None"
    email: str = "None"
    enabled: bool = True

    orders: List[Order]  # order_FK_1
    regions: List[Region]

    def __init__(self, id: int = 0, name: str = "", email: str = "None", enabled: bool = True):
        self.id = id
        self.name = name
        self.email = email
        self.enabled = enabled
        self.orders: List[Order] = list()
        self.regions: List[Region] = list()

    def map_row(self, row) -> TableBase:
        self.id = row[0]
        self.name = row[1]
        self.email = row[2]
        self.enabled = TableBase.int_to_bool(row[3])
        return self

    def get_insert_params(self) -> {}:
        return {"name": self.name, "email": self.email, "enabled": TableBase.bool_to_int(self.enabled)}

    def get_update_params(self) -> {}:
        return {"name": self.name, "email": self.email, "enabled": TableBase.bool_to_int(self.enabled), "id": self.id}


class CustomerRegion(TableBase):
    __table_name__ = "customerregion"
    __drop_script__ = ""
    __create_script__ = "create table \"customerregion\" (\"customerid\" INTEGER ,\"regionid\" INTEGER ,PRIMARY KEY (\"customerid\", \"regionid\")); CREATE INDEX \"customeregion_customer_IDX\" ON \"customerregion\" (\"customerid\");CREATE INDEX \"customeregion_region_IDX\" ON \"customerregion\" (\"regionid\");"
    __table_exists_script__ = "SELECT name FROM sqlite_schema WHERE type='table' and name = 'customerregion'"
    __table_count_script__ = "select count(*) from \"customerregion\""
    __insert_script__ = "insert into \"customerregion\" (\"customerid\", \"regionid\") values (:customerid, :regionid);"
    __update_script__ = ""
    __delete_script__ = "delete from \"customerregion\" where \"customerid\" = :customerid and \"regionid\" = :regionid;"
    __fetch_by_id_script__ = "select \"customerid\", \"regionid\" from \"customerregion\" where \"customerid\" = :customerid and \"regionid\" = :regionid;"
    __item_exists_script__ = "select count(*) from \"customerregion\" where \"customerid\" = :customerid and \"regionid\" = :regionid;"

    customer_id: int = 0
    region_id: int = 0

    def __init__(self, customer_id: int = 0, region_id: int = 0, ):
        self.customer_id = customer_id
        self.region_id = region_id

    def map_row(self, row) -> TableBase:
        self.customer_id = row[0]
        self.region_id = row[1]
        return self

    def get_insert_params(self) -> {}:
        return {"customerid": self.customer_id, "regionid": self.region_id}

    def get_update_params(self) -> {}:
        return {}


class Order(TableBase):
    __table_name__ = "order"
    __drop_script__ = "None"
    __create_script__ = "create table \"order\" (\"id\" INTEGER ,\"customerid\" INTEGER ,\"createdate\" REAL ,\"orderstatusid\" INTEGER ,\"totalprice\" REAL ,PRIMARY KEY (\"id\"),FOREIGN KEY (\"orderstatusid\") REFERENCES \"orderstatus\"(\"id\"),FOREIGN KEY (\"customerid\") REFERENCES \"customer\"(\"id\")); CREATE INDEX \"order_FK\" ON \"order\" (\"orderstatusid\"); CREATE INDEX \"order_FK_1\" ON \"order\" (\"customerid\");"
    __table_exists_script__ = "SELECT name FROM sqlite_schema WHERE type='table' and name = 'order'"
    __table_count_script__ = "select count(*) from \"order\""
    __insert_script__ = "insert into \"order\" (\"customerid\", \"createdate\", \"orderstatusid\", \"totalprice\") values (:customerid, :createdate, :orderstatusid, :totalprice);"
    __update_script__ = "update \"order\" set \"customerid\" = :customerid, \"createdate\" = :createdate, \"orderstatusid\" = :orderstatusid, \"totalprice\" = :totalprice where \"id\" = :id;"
    __delete_script__ = "delete from \"order\" where \"id\" = :id;"
    __fetch_by_id_script__ = "select \"id\", \"customerid\", \"createdate\", \"orderstatusid\", \"totalprice\" from \"order\" where \"id\" = :id;"
    __item_exists_script__ = "select count(*) from \"order\" where \"id\" = :id;"

    id: int = 0
    customer_id: int = 0
    create_date: datetime = datetime.min
    order_status_id: int = 0
    total_price: float = 0

    order_lines: List[OrderLine]  # orderline_FK

    def __init__(self, id: int = 0, customer_id: int = 0, create_date: datetime = datetime.min,
                 order_status_id: int = 0, total_price: float = 0):
        self.id = id
        self.customer_id = customer_id
        self.create_date = create_date
        self.order_status_id = order_status_id
        self.total_price = total_price
        self.order_lines: List[OrderLine] = list()

    def map_row(self, row) -> TableBase:
        self.id = row[0]
        self.customer_id = row[1]
        self.create_date = TableBase.float_to_datetime(row[2])
        self.order_status_id = row[3]
        self.total_price = row[4]
        return self

    def get_insert_params(self) -> {}:
        return {"customerid": self.customer_id, "createdate": TableBase.datetime_to_float(self.create_date),
                "orderstatusid": self.order_status_id, "totalprice": self.total_price}

    def get_update_params(self) -> {}:
        return {"customerid": self.customer_id, "createdate": TableBase.datetime_to_float(self.create_date),
                "orderstatusid": self.order_status_id, "totalprice": self.total_price, "id": self.id}

    # end-autogenerated

    def calc_price(self):
        self.total_price = sum([ol.price * ol.quantity for ol in self.order_lines])


class OrderLine(TableBase):
    __table_name__ = "orderline"
    __drop_script__ = "None"
    __create_script__ = "create table \"orderline\" (\"id\" INTEGER ,\"orderid\" INTEGER ,\"productid\" INTEGER ,\"quantity\" REAL ,\"price\" REAL ,PRIMARY KEY (\"id\"),FOREIGN KEY (\"orderid\") REFERENCES \"order\"(\"id\"),FOREIGN KEY (\"productid\") REFERENCES \"product\"(\"id\")); CREATE INDEX \"orderline_FK\" ON \"orderline\" (\"orderid\"); CREATE INDEX \"orderline_FK_1\" ON \"orderline\" (\"productid\");"
    __table_exists_script__ = "SELECT name FROM sqlite_schema WHERE type='table' and name = 'orderline'"
    __table_count_script__ = "select count(*) from \"orderline\""
    __insert_script__ = "insert into \"orderline\" (\"orderid\", \"productid\", \"quantity\", \"price\") values (:orderid, :productid, :quantity, :price);"
    __update_script__ = "update \"orderline\" set \"orderid\" = :orderid, \"productid\" = :productid, \"quantity\" = :quantity, \"price\" = :price where \"id\" = :id;"
    __delete_script__ = "delete from \"orderline\" where \"id\" = :id;"
    __fetch_by_id_script__ = "select \"id\", \"orderid\", \"productid\", \"quantity\", \"price\" from \"orderline\" where \"id\" = :id;"
    __item_exists_script__ = "select count(*) from \"orderline\" where \"id\" = :id;"

    id: int = 0
    order_id: int = 0
    product_id: int = 0
    quantity: float = 0
    price: float = 0

    def __init__(self, id: int = 0, order_id: int = 0, product_id: int = 0, quantity: float = 0, price: float = 0):
        self.id = id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price

    def map_row(self, row) -> TableBase:
        self.id = row[0]
        self.order_id = row[1]
        self.product_id = row[2]
        self.quantity = row[3]
        self.price = row[4]
        return self

    def get_insert_params(self) -> {}:
        return {"orderid": self.order_id, "productid": self.product_id, "quantity": self.quantity, "price": self.price}

    def get_update_params(self) -> {}:
        return {"orderid": self.order_id, "productid": self.product_id, "quantity": self.quantity, "price": self.price,
                "id": self.id}


class OrderStatus(TableBase):
    __table_name__ = "orderstatus"
    __drop_script__ = "None"
    __create_script__ = "create table \"orderstatus\" (\"id\" INTEGER ,\"value\" TEXT ,PRIMARY KEY (\"id\")); CREATE UNIQUE INDEX \"orderstatus_UN\" ON \"orderstatus\" (\"value\");"
    __table_exists_script__ = "SELECT name FROM sqlite_schema WHERE type='table' and name = 'orderstatus'"
    __table_count_script__ = "select count(*) from \"orderstatus\""
    __insert_script__ = "insert into \"orderstatus\" (\"value\") values (:value);"
    __update_script__ = "update \"orderstatus\" set \"value\" = :value where \"id\" = :id;"
    __delete_script__ = "delete from \"orderstatus\" where \"id\" = :id;"
    __fetch_by_id_script__ = "select \"id\", \"value\" from \"orderstatus\" where \"id\" = :id;"
    __item_exists_script__ = "select count(*) from \"orderstatus\" where \"id\" = :id;"

    id: int = 0
    value: str = "None"

    def __init__(self, id: int = 0, value: str = "None"):
        self.id = id
        self.value = value

    def map_row(self, row) -> TableBase:
        self.id = row[0]
        self.value = row[1]
        return self

    def get_insert_params(self) -> {}:
        return {"value": self.value}

    def get_update_params(self) -> {}:
        return {"value": self.value, "id": self.id}


class Product(TableBase):
    __table_name__ = "product"
    __drop_script__ = "None"
    __create_script__ = "create table \"product\" (\"id\" INTEGER ,\"name\" TEXT ,\"enabled\" INTEGER ,\"price\" REAL ,PRIMARY KEY (\"id\")); CREATE UNIQUE INDEX \"product_UN\" ON \"product\" (\"name\");"
    __table_exists_script__ = "SELECT name FROM sqlite_schema WHERE type='table' and name = 'product'"
    __table_count_script__ = "select count(*) from \"product\""
    __insert_script__ = "insert into \"product\" (\"name\", \"enabled\", \"price\") values (:name, :enabled, :price);"
    __update_script__ = "update \"product\" set \"name\" = :name, \"enabled\" = :enabled, \"price\" = :price where \"id\" = :id;"
    __delete_script__ = "delete from \"product\" where \"id\" = :id;"
    __fetch_by_id_script__ = "select \"id\", \"name\", \"enabled\", \"price\" from \"product\" where \"id\" = :id;"
    __item_exists_script__ = "select count(*) from \"product\" where \"id\" = :id;"

    id: int = 0
    name: str = "None"
    enabled: bool = True
    price: float = 0

    def __init__(self, id: int = 0, name: str = "None", enabled: bool = True, price: float = 0):
        self.id = id
        self.name = name
        self.enabled = enabled
        self.price = price

    def map_row(self, row) -> TableBase:
        self.id = row[0]
        self.name = row[1]
        self.enabled = TableBase.int_to_bool(row[2])
        self.price = row[3]
        return self

    def get_insert_params(self) -> {}:
        return {"name": self.name, "enabled": TableBase.bool_to_int(self.enabled), "price": self.price}

    def get_update_params(self) -> {}:
        return {"name": self.name, "enabled": TableBase.bool_to_int(self.enabled), "price": self.price, "id": self.id}


class Region(TableBase):
    __table_name__ = "region"
    __drop_script__ = "None"
    __create_script__ = "create table \"region\" (\"id\" INTEGER ,\"name\" TEXT ,PRIMARY KEY (\"id\")); CREATE INDEX \"region_name_IDX\" ON \"region\" (\"name\");"
    __table_exists_script__ = "SELECT name FROM sqlite_schema WHERE type='table' and name = 'region'"
    __table_count_script__ = "select count(*) from \"region\""
    __insert_script__ = "insert into \"region\" (\"id\", \"name\") values (:name);"
    __update_script__ = "update \"region\" set \"name\" = :name where \"id\" = :id;"
    __delete_script__ = "delete from \"region\" where \"id\" = :id;"
    __fetch_by_id_script__ = "select \"id\", \"name\" from \"region\" where \"id\" = :id;"
    __item_exists_script__ = "select count(*) from \"region\" where \"id\" = :id;"

    id: int = 0
    name: str = ""
    customers: List[Customer]

    def __init__(self, id: int = 0, name: str = ""):
        self.id = id
        self.name = name
        self.customers: List[Customer] = list()

    def map_row(self, row) -> TableBase:
        self.id = row[0]
        self.name = row[1]
        return self

    def get_insert_params(self) -> {}:
        return {"name": self.name}

    def get_update_params(self) -> {}:
        return {"name": self.name, "id": self.id}
