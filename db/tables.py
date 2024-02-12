from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from db.database import DBBase


class Users(DBBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)
    is_admin = Column(Boolean, default=False)


class Items(DBBase):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    belongs_to_id = Column(Integer, ForeignKey("users.id"))
