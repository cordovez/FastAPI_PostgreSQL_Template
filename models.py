from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
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


class Delivery(StrEnum):
    FACE_TO_FACE_ON_PREMISES = "face-to-face at academy"
    FACE_TO_FACE_MY_PLACE = "face-to-face my place"
    DISTANCE_LEARNING = "distance learning"


class Levels(StrEnum):
    A1 = auto()
    A2 = auto()
    B1 = auto()
    B2 = auto()
    C1 = auto()
    C2 = auto()


""" 
Link Table
"""


class StudentEnrollment(SQLModel, table=True):
    enrollment_id: Optional[int] = Field(
        default=None, foreign_key="enrollmentdb.id", primary_key=True
    )

    student_id: Optional[int] = Field(
        default=None, foreign_key="studentdb.id", primary_key=True
    )


"""
Courses

"""


class EnrollmentBase(SQLModel):
    course_id: int = Field(foreign_key="coursedb.id")
    course_name: str
    student_id: int = Field(foreign_key="studentdb.id")
    instructor_id: int = Field(foreign_key="coursedb.id")
    start_level: Levels = Field(default=Levels.A1)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    week_days: Optional[str] = None
    time_start: Optional[str] = None
    time_end: Optional[str] = None


class EnrollmentDB(EnrollmentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    students: List["StudentDB"] = Relationship(
        back_populates="enrollments", link_model=StudentEnrollment
    )


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentRead(EnrollmentBase):
    id: int


class EnrollmentUpdate(EnrollmentBase):
    course_id: Optional[int] = None
    student_id: Optional[int] = None
    instructor_id: Optional[int] = None
    start_level: Optional[Levels] = None


"""
Courses

"""


class CourseBase(SQLModel):
    course_name: str = Field(default=None, index=True, unique=True)
    description: Optional[str] = Field(default=None)


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
    primary_contact: Optional[str] = Field(default=None)
    secondary_contact: Optional[str] = Field(default=None)
    street_address: Optional[str] = Field(default=None)
    post_code: Optional[str] = Field(default=None)
    locality: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)


class PersonDB(PersonBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hashed: Optional[str] = Field(default=None)

    role: str = Field(default=Role.STUDENT)


class StudentDB(PersonBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    role: str = Field(default=Role.STUDENT)

    enrollments: List[EnrollmentDB] = Relationship(
        back_populates="students", link_model=StudentEnrollment
    )


class PersonRead(PersonBase):
    id: int
    role: Role


class PersonCreate(SQLModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str


class PersonUpdate(PersonBase):
    username: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class PersonUpdateRole(SQLModel):
    role: Role = Field(default=Role.STUDENT)
