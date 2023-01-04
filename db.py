from sqlmodel import create_engine, SQLModel
from dotenv import load_dotenv
import os



load_dotenv()

mysqlstr = os.getenv("DBURL")



engine = create_engine(mysqlstr, echo=True)
SQLModel.metadata.create_all(engine)

