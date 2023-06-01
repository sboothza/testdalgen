from src.base.session import Session
from src.base.repository_base import RepositoryBase
from src.entities.test_table import TestTable


class TestTableRepository(RepositoryBase):
    __table__ = TestTable
    
    def get_by_id(self, session: Session, id: int):
        item: TestTable = self._get_by_id(session, {"id": id})
        return item
        
    def exists(self, session: Session, id: int):
        return self._item_exists(session, {"id": id})
        
    def delete(self, session: Session, id: int):
        self._delete(session, {"id": id})
        
    def add(self, session: Session, item: TestTable):
        id = self._execute_lastrowid(session, item.__insert_script__, item.get_insert_params())
        item.id = id
    
    

# end-autogenerated