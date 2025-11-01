from sqlalchemy import create_engine as ce
from sqlalchemy.orm import sessionmaker as sm, declarative_base as dec
from dotenv import load_dotenv as ld
import os

ld("env\.env")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print(SQLALCHEMY_DATABASE_URL)

engine = ce(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

LocalSession = sm(autocommit=False, autoflush= False, bind=engine)

Base = dec()

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()