#import os
#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
#from  sqlalchemy.ext.declarative import declarative_base
#
#SQLALCHEMY_DB_URL = os.getenv("POSTGRES_CONNECTION")
#
#engine =  create_engine(SQLALCHEMY_DB_URL)
#
#Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#Base = declarative_base()