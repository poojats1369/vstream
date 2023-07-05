import os
from dotenv import load_dotenv
# from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
        os.environ.get('POSTGRES_USER'),
        os.environ.get('POSTGRES_PASS'),
        os.environ.get('POSTGRES_HOST'),
        os.environ.get('POSTGRES_DB')
    )
engine = create_engine(SQLALCHEMY_DATABASE_URI)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

# # MONGODB_DATABASE_URI='mongodb://{}:{}/'.format(
# #     os.environ.get('MONGODB_HOST'),
# #     os.environ.get('MONGODB_PORT')
# #     )

# MONGODB_DATABASE_URI = 'mongodb://{}:{}/'.format(
#     os.environ.get('MONGODB_HOST'),
#     int(os.environ.get('MONGODB_PORT'))  # Convert port to integer
# )

# mymongo = MongoClient(MONGODB_DATABASE_URI)