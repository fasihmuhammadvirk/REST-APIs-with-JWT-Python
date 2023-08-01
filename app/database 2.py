
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

#also replace this database url in the alembic.ini file 
database_url = 'postgresql://postgres:1213@localhost:5432/practice_database'

#after update the model file to run migration use the commands 
# cmd:  alembic revision --autogenerate -m "Create Items Table"
# cmd: alembic upgrade head

engine = create_engine(database_url,echo = True)
session = sessionmaker(bind=engine)