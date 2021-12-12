import logging
from app.models import User, GroupPurchase, GroupIncome, Purchase, Income
from app.db import engine


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
)


def drop_tables():
    User.metadata.drop_all(engine)
    GroupPurchase.metadata.drop_all(engine)
    GroupIncome.metadata.drop_all(engine)
    Purchase.metadata.drop_all(engine)
    Income.metadata.drop_all(engine)


def create_tables():
    User.metadata.create_all(engine)
    GroupPurchase.metadata.create_all(engine)
    GroupIncome.metadata.create_all(engine)
    Purchase.metadata.create_all(engine)
    Income.metadata.create_all(engine)


if __name__ == '__main__':
    print("Start")
    drop_tables()
    create_tables()
    print("End")

