from sqlalchemy.orm import Session
from domain.unit_of_work import UnitOfWork

class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session:Session):
        self.session = session

    def __enter__(self):
        self.session.begin()
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.session.close()
    
    def commit(self):
        self.session.commit()
   
    def rollback(self):
        self.session.rollback()