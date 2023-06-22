import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv('DATABASE_URL')
if 'postgres://' in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://')

engine = create_engine(DATABASE_URL)
Session = sessionmaker(engine)
