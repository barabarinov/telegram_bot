import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, GroupPurchase, GroupIncome, Purchase, Income

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
)

if __name__ == '__main__':
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')

    # User.metadata.drop_all(engine)
    # GroupPurchase.metadata.drop_all(engine)
    # GroupIncome.metadata.drop_all(engine)
    # Purchase.metadata.drop_all(engine)
    # Income.metadata.drop_all(engine)

    # User.metadata.create_all(engine)
    # GroupPurchase.metadata.create_all(engine)
    # GroupIncome.metadata.create_all(engine)
    # Purchase.metadata.create_all(engine)
    # Income.metadata.create_all(engine)

    Session = sessionmaker(engine)
