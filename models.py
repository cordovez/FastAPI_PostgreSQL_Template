from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from enum import Enum, auto, StrEnum
from sqlalchemy import Column, String
from pydantic import BaseModel, EmailStr


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


class BookUpdate(BookCreate):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    password: Optional[str] = None
    editor: Optional[str] = None
    isbn: Optional[str] = None
    language: Optional[str] = None


class TeamBase(SQLModel):
    name: str = Field(index=True)
    headquarters: str


"""
TEAMS
"""


class Team(TeamBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    heroes: list["Hero"] = Relationship(back_populates="team")


class TeamCreate(TeamBase):
    pass


class TeamRead(TeamBase):
    id: int


class TeamUpdate(SQLModel):
    name: Optional[str] = None
    headquarters: Optional[str] = None


"""
Persons
"""


class Role(StrEnum):
    ACADEMIC_ADMIN = auto()
    TECH_ADMIN = auto()
    INSTRUCTOR = auto()
    STUDENT = auto()
    STAFF = auto()


class PersonBase(SQLModel):
    username: str = Field(index=True)
    email: str = Field(index=True)
    first_name: str
    middle_name: Optional[str] = Field(default=None)
    last_name: str = Field(index=True)
    role: str
    primary_contact: Optional[str] = Field(default=None)
    secondary_contact: Optional[str] = Field(default=None)
    street_address: Optional[str] = Field(default=None)
    post_code: Optional[str] = Field(default=None)
    locality: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)


class PersonDB(PersonBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hashed: Optional[str] = Field(default=None)


class PersonRead(PersonBase):
    id: int


class PersonCreate(SQLModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str


class PersonUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    primary_contact: Optional[str] = None
    secondary_contact: Optional[str] = None
    street_address: Optional[str] = None
    post_code: Optional[str] = None
    locality: Optional[str] = None
    country: Optional[str] = None


class Login(SQLModel):
    username: str
    password: str


"""
Heroes
"""


class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

    team_id: Optional[int] = Field(default=None, foreign_key="team.id")


class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    team: Optional[Team] = Relationship(back_populates="heroes")


class HeroRead(HeroBase):
    id: int


class HeroCreate(HeroBase):
    pass


class HeroUpdate(SQLModel):
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None
    team_id: Optional[int] = None
