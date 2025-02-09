from hmac import new
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from domain.models import Product
from domain.services import WarehouseService
from infrastructure.orm import Base, ProductORM, OrderORM
from infrastructure.repositories import SqlAlchemyProductRepository, SqlAlchemyOrderRepository
from infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from infrastructure.database import DATABASE_URL

engine= create_engine(DATABASE_URL)
SessionFactory=sessionmaker(bind=engine)
Base.metadata.create_all(engine)

def main():
    session = SessionFactory()
    product_repo = SqlAlchemyProductRepository(session)
    order_repo = SqlAlchemyOrderRepository(session)

    uow = SqlAlchemyUnitOfWork(session)

    warehouse_service = WarehouseService(product_repo, order_repo)
    with uow:
        new_product = warehouse_service.create_product(name="test1", quantity=1, price=100)
        new_product2 = warehouse_service.create_product(name="test2", quantity=2, price=200)
        
        print(f"create product: {new_product}")

        warehouse_service.create_order([new_product])
        warehouse_service.create_order([new_product,new_product2])
        print("create orders")
        #todo add some actions
        print("pre commit state",warehouse_service.list_orders())
        print (warehouse_service.list_products())
        
        

        uow.commit()

        print("post commit state",warehouse_service.list_orders())

if __name__ == "__main__":
    main()


