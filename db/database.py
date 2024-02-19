from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.getenv("DB_URL")

engine = create_engine(DB_URL, echo=True)


#  this is SQLModel when using
# DBBase = declarative_base()


# def get_db():
#     db = SessionLocal()

#     try:
#         yield db

#     finally:
#         db.close()
