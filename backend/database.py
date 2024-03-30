import os
import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
#!### end imports #####################################


#! Configuration
load_dotenv()
SQLALCHEMY_DATABASE_URL = os.environ.get('SQLALCHEMY_DATABASE_URL')


# DATABASE_HOST = os.environ.get('DATABASE_HOST')
# DATABASE_NAME = os.environ.get('DATABASE_NAME')
# DATABASE_USER = os.environ.get('DATABASE_USER')
# DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
# # SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"


#! Define engine and session
engine = None
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


#! Establish database connection
while engine is None:
    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        print("Database connected successfully!")  # Print success message
    except OperationalError as e:
        print(f"Failed to connect to the database: {e}")
        print("Retrying in 5 seconds...")
        time.sleep(5)


#! Define session generator function
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
