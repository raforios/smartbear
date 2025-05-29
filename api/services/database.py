'''
    Database connection service
'''
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import dotenv_values

PARAMETERS = dotenv_values('.env')

Base: DeclarativeMeta = declarative_base()

# Configure the engine with PostgreSQL connection details
engine = create_engine(PARAMETERS['DATABASE_URL'])

# Create a session factory for interacting with the database
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

# Dependency to provide a database session
def get_db():
    '''
        Get DB Connection through SQLALCHEMY
    '''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
