import unittest
from datetime import datetime

from entities.entities import OrderStatus, Product, Customer, Order, OrderLine
from src.base.session import SessionFactory
from config import Config

import src.repositories.customer_region_repository
import src.repositories.customer_repository
import src.repositories.order_line_repository
import src.repositories.order_repository
import src.repositories.order_status_repository
import src.repositories.product_repository
import src.repositories.region_repository


class ReferentialTests(unittest.TestCase):
    def setUp(self) -> None:
        # self.config = Config("mysql://root:or9asm1c@localhost/test2")
        self.config = Config("sqlite://~/test.db")
        with SessionFactory.connect(self.config.connection_string) as session:
            self.orderstatus_repo = src.repositories.order_status_repository.OrderStatusRepository()
            if not self.orderstatus_repo.schema_exists(session):
                self.orderstatus_repo.create_schema(session)

            self.product_repo = src.repositories.product_repository.ProductRepository()
            if not self.product_repo.schema_exists(session):
                self.product_repo.create_schema(session)

            self.customer_region_repo = src.repositories.customer_region_repository.CustomerRegionRepository()
            if not self.customer_region_repo.schema_exists(session):
                self.customer_region_repo.create_schema(session)

            self.orderline_repo = src.repositories.order_line_repository.OrderLineRepository()
            if not self.orderline_repo.schema_exists(session):
                self.orderline_repo.create_schema(session)

            self.order_repo = src.repositories.order_repository.OrderRepository(self.orderline_repo)
            if not self.order_repo.schema_exists(session):
                self.order_repo.create_schema(session)

            self.customer_repo = src.repositories.customer_repository.CustomerRepository(self.order_repo,
                                                                                         self.customer_region_repo)
            if not self.customer_repo.schema_exists(session):
                self.customer_repo.create_schema(session)

            self.region_repo = src.repositories.region_repository.RegionRepository(self.customer_region_repo)
            if not self.region_repo.schema_exists(session):
                self.region_repo.create_schema(session)

    def test_connect(self):
        with SessionFactory.connect(self.config.connection_string) as session:
            self.assertTrue(self.orderstatus_repo.schema_exists(session))
            self.assertTrue(self.product_repo.schema_exists(session))
            self.assertTrue(self.customer_repo.schema_exists(session))
            self.assertTrue(self.order_repo.schema_exists(session))
            self.assertTrue(self.orderline_repo.schema_exists(session))
            self.assertTrue(self.region_repo.schema_exists(session))
            self.assertTrue(self.customer_region_repo.schema_exists(session))

    def test_dropall(self):
        with SessionFactory.connect(self.config.connection_string) as session:
            self.orderline_repo.drop_schema(session)
            self.order_repo.drop_schema(session)
            self.customer_repo.drop_schema(session)
            self.product_repo.drop_schema(session)
            self.orderstatus_repo.drop_schema(session)

    def test_init(self):
        with SessionFactory.connect(self.config.connection_string) as session:
            self.orderstatus_repo.add(session, OrderStatus(value="created"))
            self.orderstatus_repo.add(session, OrderStatus(value="processed"))
            self.orderstatus_repo.add(session, OrderStatus(value="fulfilled"))
            self.orderstatus_repo.add(session, OrderStatus(value="cancelled"))

            self.product_repo.add(session, Product(name="coffee", price=80))
            self.product_repo.add(session, Product(name="tea", price=30))
            self.product_repo.add(session, Product(name="milk", price=20))
            self.product_repo.add(session, Product(name="bread", price=15))
            self.product_repo.add(session, Product(name="water", price=10))
            self.product_repo.add(session, Product(name="biscuits", price=60))

            self.customer_repo.add(session, Customer(name="Bob", email="bob@bob.com"))
            self.customer_repo.add(session, Customer(name="Bill", email="bill@bill.com"))

    def test_order(self):
        with SessionFactory.connect(self.config.connection_string) as session:
            customer: Customer = self.customer_repo.get_by_name(session, "Bob")
            order_status: OrderStatus = self.orderstatus_repo.get_by_name(session, "created")
            product: Product = self.product_repo.get_by_name(session, "milk")
            order: Order = Order(customer_id=customer.id, create_date=datetime.now(),
                                                                       order_status_id=order_status.id)
            order.order_lines.append(
                OrderLine(order_id=order.id, product_id=product.id, quantity=1, price=product.price))
            order.order_lines.append(OrderLine(order_id=order.id, product_id=product.id, quantity=2,
                                                                       price=product.price * 2))
            order.calc_price()
            self.order_repo.add(session, order)

            new_order = self.order_repo.get_by_id(session, order.id)
            self.assertEqual(order.customer_id, new_order.customer_id)
            self.assertEqual(order.total_price, new_order.total_price)
            self.assertEqual(len(order.order_lines), len(new_order.order_lines))


if __name__ == '__main__':
    unittest.main()
