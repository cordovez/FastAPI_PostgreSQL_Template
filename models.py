from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from enum import auto, StrEnum
from sqlalchemy import Column, String
from pydantic import BaseModel, EmailStr


"""
Persons
"""


class Role(StrEnum):
    ACADEMIC_ADMIN = auto()
    TECH_ADMIN = auto()
    INSTRUCTOR = auto()
    STUDENT = auto()
    STAFF = auto()


class Subject(StrEnum):
    FRENCH = auto()
    GERMAN = auto()
    ITALIAN = auto()
    ENGLISH = auto()
    SPANISH = auto()


class CourseBase(SQLModel):
    course_name: str = Field(default=None, index=True, unique=True)


class CourseDB(CourseBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class CourseRead(CourseBase):
    id: int
    course_name: str


class CourseCreate(CourseBase):
    course_name: Optional[str]


class CourseUpdate(CourseBase):
    course_name: Optional[str]


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
    course: Optional[str] = Field(default=None, foreign_key="coursedb.course_name")


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


class PersonCourseUpdate(SQLModel):
    course: str


class TeamBase(SQLModel):
    name: str = Field(index=True)
    headquarters: str


class Team(TeamBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    heroes: List["Hero"] = Relationship(back_populates="team")


class TeamCreate(TeamBase):
    pass


class TeamRead(TeamBase):
    id: int


class TeamUpdate(SQLModel):
    name: Optional[str] = None
    headquarters: Optional[str] = None


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
