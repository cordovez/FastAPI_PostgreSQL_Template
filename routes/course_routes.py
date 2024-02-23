from fastapi import Depends, HTTPException, APIRouter, status, Query
from db.database import engine
from models import (
    PersonCreate,
    PersonRead,
    PersonUpdate,
    PersonDB,
    Role,
    CourseRead,
    CourseCreate,
    CourseDB,
    CourseUpdate,
    Subject,
)
from sqlmodel import select, Session

course_router = APIRouter()


def get_session():
    with Session(engine) as session:
        yield session


@course_router.get(
    "/all", response_model=list[CourseRead], status_code=status.HTTP_200_OK
)
async def get_all_courses(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    return session.exec(select(CourseDB).offset(offset).limit(limit)).all()


@course_router.get(
    "/{course_id}", response_model=CourseRead, status_code=status.HTTP_200_OK
)
async def get_one_user(
    *,
    session: Session = Depends(get_session),
    course_id: int,
):
    if course := session.get(CourseDB, course_id):
        return course
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@course_router.post("/add", status_code=status.HTTP_201_CREATED)
async def create_a_course(
    *,
    session: Session = Depends(get_session),
    new_course: CourseCreate,
    subject: Subject,
):
    """
    Courses are created from the values of the Enum passed as "subject". The body of the post request is for future possible fields
    """
    extra_data = {"course_name": subject}
    cousedb = CourseDB.model_validate(new_course, update=extra_data)
    session.add(cousedb)
    session.commit()
    session.refresh(cousedb)
    return cousedb


@course_router.patch("/update/{course_id}", response_model=CourseRead)
async def update_a_course(
    *,
    session: Session = Depends(get_session),
    course_id: int,
    new_details: CourseUpdate,
):
    """
    The update path is intended for other fields that may be created eventually, whereas the 'course_name' should probably remain a value from an enum.
    """
    db_course = session.get(CourseDB, course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = new_details.model_dump(exclude_unset=True)

    db_course.sqlmodel_update(update_data)
    session.add(db_course)
    session.commit()
    session.refresh(db_course)
    return db_course


@course_router.delete("/delete/{course_id}")
async def delete_course(
    *,
    session: Session = Depends(get_session),
    course_id: int,
):
    course = session.get(CourseDB, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    session.delete(course)
    session.commit()
    return {"deleted": True}
