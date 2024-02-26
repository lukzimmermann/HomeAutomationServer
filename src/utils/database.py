import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(os.getenv("POSTGRES_CONNECTION"))

session = sessionmaker(bind=engine)

def get_db():
    database = session()
    try:
        yield database
    finally:
        database.close()