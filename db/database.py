from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.getenv("DB_URL")

engine = create_engine(DB_URL, echo=True)


# SessionLocal = sessionmaker(autoflush=False, bind=engine)

#  this is SQLModel when using
# DBBase = declarative_base()


# def get_db():
#     db = SessionLocal()

#     try:
#         yield db

#     finally:
#         db.close()
