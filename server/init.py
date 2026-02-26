import os
from fastapi import FastAPI
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()


app=FastAPI()
base=declarative_base()
engine=create_engine(url=os.getenv('SQLITE_DB_URI'))
session=sessionmaker(bind=engine)
db_con_obj=session()
