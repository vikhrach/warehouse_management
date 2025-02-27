from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from domain.services import WarehouseService
from infrastructure.database import DATABASE_URL
from infrastructure.orm import Base
from infrastructure.repositories import SqlAlchemyOrderRepository, SqlAlchemyProductRepository
from infrastructure.unit_of_work import SqlAlchemyUnitOfWork

engine = create_engine(DATABASE_URL)
SessionFactory = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


def main():
    session = SessionFactory()
    product_repo = SqlAlchemyProductRepository(session)
    order_repo = SqlAlchemyOrderRepository(session)

    uow = SqlAlchemyUnitOfWork(session)

    warehouse_service = WarehouseService(product_repo, order_repo)

    with uow:
        print("Начало создания продуктов")
        new_product_test1 = warehouse_service.create_product(name="test1", quantity=1, price=100)
        new_product_test2 = warehouse_service.create_product(name="test2", quantity=2, price=200)

        print(f"Продукты созданы {new_product_test1} {new_product_test1}")
        print(f"Продукты в сессии {warehouse_service.list_products()}")

        print("Начало создания заказов")
        order_test1 = warehouse_service.create_order([new_product_test1])
        order_test2 = warehouse_service.create_order([new_product_test1, new_product_test2])
        print("Заказы созданы", order_test1, order_test2)
        print("Заказы в сессии", warehouse_service.list_orders())

        print("Коммит не вызван данные в БД не записаны")

    with uow:
        print(warehouse_service.list_products())
        print(warehouse_service.list_orders())

        print("Начало создания продуктов")
        new_product_test1 = warehouse_service.create_product(name="test1", quantity=1, price=100)
        new_product_test2 = warehouse_service.create_product(name="test2", quantity=2, price=200)

        print(f"Продукты созданы {new_product_test1} {new_product_test1}")
        print(f"Продукты в сессии {warehouse_service.list_products()}")

        print("Начало создания заказов")
        order_test1 = warehouse_service.create_order([new_product_test1])
        order_test2 = warehouse_service.create_order([new_product_test1, new_product_test2])
        print("Заказы созданы", order_test1, order_test2)
        print("Заказы в сессии", warehouse_service.list_orders())
        uow.commit()

    with uow:
        print("Проверить наличие записей в базе после коммита")
        print(warehouse_service.list_products())
        print(warehouse_service.list_orders())


if __name__ == "__main__":
    main()
