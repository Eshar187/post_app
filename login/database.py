from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
# from .config import settings




SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:Eshar#4787@Localhost:5432/postgres'
# SQLALCHEMY_DATABASE_URL = f'postgresql://{database_username}:{database_password}@{database_hostname}:{database_port}/{database_name}'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
  
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()

try:
    connec = psycopg2.connect(host='Localhost',database='postgres',user='postgres',password='Eshar#4787',cursor_factory= RealDictCursor)
    cursor = connec.cursor()
    print("Database connection was succesfull!")
    # break
except Exception as error:
    print("Connecting to database failed")
    print("Error: ", error)


