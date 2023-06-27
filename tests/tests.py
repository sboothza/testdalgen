import random
import string
import time
import unittest
from datetime import datetime

from dateutil.parser import parse

from base.session import SessionFactory
from config import Config
from entities.order_status import OrderStatus
from repositories.order_status_repository import OrderStatusRepository
from src.repositories.test_table_repository import TestTableRepository


class TestMe:
    @staticmethod
    def test_static():
        print("static")


class SessionTests(unittest.TestCase):
    def setUp(self) -> None:
        # self.config = Config("~/internal/src/sboothza/testdalgen/db.db")
        #self.config = Config("sqlite://file::memory:?cache=shared")

        # self.config = Config("mysql://root:or9asm1c@localhost/test2")

        self.config = Config("pgsql://postgres:or9asm1c@localhost/test")

    @staticmethod
    def random_string(len: int) -> str:
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for _ in range(len))

    # @staticmethod
    # def build_random_item(item: TestTable):
    #     item.string_field = SessionTests.random_string(10)
    #     item.string_field2 = SessionTests.random_string(10)
    #     item.int_field = random.randint(0, 100)
    #     item.float_field = random.uniform(0, 100)
    #     item.bool_field = random.randint(0, 2) == 1
    #     item.date_time_field = datetime.now()

    # def test_commit(self):
    #     with SessionFactory.connect(self.config.connection_string) as session:
    #         item = TestTable()
    #         SessionTests.build_random_item(item)
    #         with session.fetch(TestTable.__insert_script__, item.get_insert_params()) as cursor:
    #             item.id = cursor.lastrowid
    #             session.rollback()
    #
    #         with session.fetch(TestTable.__fetch_by_id_script__, {"id": item.id}) as cursor:
    #             row = cursor.fetchone()
    #             self.assertIsNone(row)
    #
    #         with session.fetch(TestTable.__insert_script__, item.get_insert_params()) as cursor:
    #             item.id = cursor.lastrowid
    #             session.commit()
    #
    #         with session.fetch(TestTable.__fetch_by_id_script__, {"id": item.id}) as cursor:
    #             row = cursor.fetchone()
    #             self.assertEqual(row[0], item.id)
    #
    # def test_commit_wrapped(self):
    #     with SessionFactory.connect(self.config.connection_string) as session:
    #         item = TestTable()
    #         repo = TestTableRepository()
    #
    #         SessionTests.build_random_item(item)
    #
    #         repo.add(session, item)
    #         session.rollback()
    #         item2 = repo.get_by_id(session, item.id)
    #         self.assertIsNone(item2)
    #
    #         repo.add(session, item)
    #         session.commit()
    #         item2 = repo.get_by_id(session, item.id)
    #         self.assertEqual(item2.id, item.id)


class BasicTests(unittest.TestCase):
    def setUp(self) -> None:
        # self.config = Config("~/internal/src/sboothza/testdalgen/db.db")
        # self.config = Config("sqlite://file::memory:?cache=shared")

        # self.config = Config("mysql://root:or9asm1c@localhost/test2")
        self.config = Config("pgsql://postgres:or9asm1c@milleniumfalcon/test")
        self.repo = OrderStatusRepository()
        with SessionFactory.connect(self.config.connection_string) as session:
            if not self.repo.schema_exists(session):
                self.repo.create_schema(session)

    def test_connect(self):
        with SessionFactory.connect(self.config.connection_string) as session:
            if not self.repo.schema_exists(session):
                self.repo.create_schema(session)

            self.assertTrue(self.repo.schema_exists(session))

    def random_string(self, len: int) -> str:
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for _ in range(len))

    def build_random_item(self, item: OrderStatus):
        item.value = self.random_string(10)

    def create_random_item(self) -> OrderStatus:
        item = OrderStatus()
        self.build_random_item(item)
        return item

    # def test_drop(self):
    #     with SessionFactory.connect(self.config.connection_string) as session:
    #         self.repo.drop_schema(session)

    def test_add(self):
        with SessionFactory.connect(self.config.connection_string) as session:
            item = self.create_random_item()
            self.repo.add(session, item)
            item2: OrderStatus = self.repo.get_by_name(session, item.value)

        self.assertEqual(item.id, item2.id)
        self.assertEqual(item.value, item2.value)


    # def test_update(self):
    #     with SessionFactory.connect(self.config.connection_string) as session:
    #         item = self.create_random_item()
    #         self.repo.add(session, item)
    #         self.build_random_item(item)
    #         self.repo.update(session, item)
    #         item2: TestTable = self.repo.get_by_id(session, item.id)
    #     self.assertEqual(item.id, item2.id)
    #     self.assertEqual(item.string_field, item2.string_field)
    #     self.assertEqual(item.int_field, item2.int_field)
    #     self.assertAlmostEqual(item.float_field, item2.float_field, 3)
    #     self.assertEqual(item.bool_field, item2.bool_field)
    #     self.assertAlmostEqual(time.mktime(item.date_time_field.timetuple()),
    #                            time.mktime(item2.date_time_field.timetuple()), delta=1)
    #
    # def test_delete(self):
    #     with SessionFactory.connect(self.config.connection_string) as session:
    #         item = self.create_random_item()
    #         self.repo.add(session, item)
    #         self.assertTrue(self.repo.exists(session, item.id))
    #         self.repo.delete(session, item.id)
    #         self.assertFalse(self.repo.exists(session, item.id))
    #
    # def test_custom(self):
    #     item = self.create_random_item()
    #     item.date_time_field = parse("2023-jan-01")
    #     self.repo.add(item)
    #     item = self.create_random_item()
    #     item.date_time_field = parse("2023-jan-01")
    #     self.repo.add(item)
    #     item = self.create_random_item()
    #     self.repo.add(item)
    #     item = self.create_random_item()
    #     self.repo.add(item)
    #     item = self.create_random_item()
    #     self.repo.add(item)
    #     item = self.create_random_item()
    #     self.repo.add(item)
    #     items = self.repo.get_before(parse("2023-feb-01"))
    #     self.assertEqual(len(items), 2)


if __name__ == '__main__':
    # unittest.main()
    tests = BasicTests()
    tests.test_add()
