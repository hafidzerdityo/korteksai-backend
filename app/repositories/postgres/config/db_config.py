from sqlalchemy import create_engine, MetaData
from databases import Database

from dotenv import load_dotenv
import os


load_dotenv('config.env')

POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST') 
POSTGRES_PORT = os.environ.get('POSTGRES_PORT') 
POSTGRES_DB = os.environ.get('POSTGRES_DB') 

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
metadata = MetaData()
database = Database(SQLALCHEMY_DATABASE_URL)