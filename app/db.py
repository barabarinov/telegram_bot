import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.getenv('DB_CONNECTION_STRING'))
Session = sessionmaker(engine)
