from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#SQLALCHEMY_DATABASE_URL='sqlite:///./todosapp.db' #create the location of the db in fastAPI application
POSTGRES_DATABASE_URL='postgresql://postgres:test1234!@localhost/BlogDatabase' #postgresql database the test1234! is the password for the database
#engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
engine = create_engine(POSTGRES_DATABASE_URL) # postgresql creating engine
SessionLocal = sessionmaker(autocommit =False, autoflush= False, bind =engine) # independent Database session 
Base = declarative_base() # will be a parent class for the model class we creating

def get_db(): # this function still stay the same in most projects, open and close the connection
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



