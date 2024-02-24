from sqlmodel import SQLModel, Field
from typing import Optional
from enum import auto, StrEnum

from pydantic import EmailStr
from datetime import date


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


"""
Courses

"""


class EnrollmentBase(SQLModel):
    student_id: int = Field(foreign_key="persondb.id")
    course_id: int = Field(foreign_key="coursedb.id")
    enrollment_date: Optional[date]


class EnrollmentDB(EnrollmentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentRead(EnrollmentBase):
    pass


"""
Courses

"""


class CourseBase(SQLModel):
    course_name: str = Field(default=None, index=True, unique=True)
    description: Optional[str] = Field(default=None)
    instructor_id: Optional[int] = Field(default=None, foreign_key="persondb.id")


class CourseDB(CourseBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class CourseRead(CourseBase):
    id: int
    course_name: str


class CourseCreate(CourseBase):
    pass


class CourseUpdate(CourseBase):
    pass


"""
Persons

"""


class PersonBase(SQLModel):
    username: str = Field(index=True, unique=True)
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
