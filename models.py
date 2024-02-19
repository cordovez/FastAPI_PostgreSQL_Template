from sqlmodel import SQLModel, Field
from typing import Optional


class BookBase(SQLModel):
    title: str = Field(index=True)
    author: str = Field(index=True)
    description: str


class Book(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field()


class BookCreate(BookBase):
    password: str


class BookRead(BookBase):
    id: int


class BookUpdate(SQLModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    password: Optional[str] = None
