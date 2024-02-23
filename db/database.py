from sqlmodel import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.getenv("SQLITE_URL")
# DB_URL = os.getenv("DB_URL")
connect_args = {"check_same_thread": False}
engine = create_engine(DB_URL, echo=True, connect_args=connect_args)
