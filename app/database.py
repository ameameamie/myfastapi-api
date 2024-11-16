from datetime import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase
from .config import settings 


class Base(DeclarativeBase):
    pass


SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# raw postgres driver establishing connection with the database 
# while True:
#     try:
#         connection = psycopg.connect(
#             host='localhost',
#             dbname='fastapi',
#             user='postgres',
#             password='amecutiepie13',
#             row_factory=dict_row)
#         cursor = connection.cursor()
#         print('Successfully connected to the database!')
#         break
#     except Exception as error:
#         print('Failed to connect to the database! Retrying in 5 seconds..')
#         print('Error:', error)
#         time.sleep(5)