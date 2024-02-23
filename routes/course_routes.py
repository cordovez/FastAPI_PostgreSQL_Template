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
    Subject,
)
from sqlmodel import select, Session

course_router = APIRouter()


def get_session():
    with Session(engine) as session:
        yield session


@course_router.get(
    "/all", response_model=list[PersonRead], status_code=status.HTTP_200_OK
)
async def get_all_users(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    return session.exec(select(PersonDB).offset(offset).limit(limit)).all()


@course_router.get(
    "/{person_id}", response_model=PersonRead, status_code=status.HTTP_200_OK
)
async def get_one_user(
    *,
    session: Session = Depends(get_session),
    person_id: int,
):
    if person := session.get(PersonDB, person_id):
        return person
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@course_router.post("/add", status_code=status.HTTP_201_CREATED)
async def create_a_course(
    *,
    session: Session = Depends(get_session),
    new_course: CourseCreate,
    subject: Subject,
):
    extra_data = {"course_name": subject}
    cousedb = CourseDB.model_validate(new_course, update=extra_data)
    session.add(cousedb)
    session.commit()
    session.refresh(cousedb)
    return cousedb


@course_router.patch("/update/{person_id}", response_model=PersonRead)
async def update_a_user(
    *,
    session: Session = Depends(get_session),
    person_id: int,
    new_details: PersonUpdate,
):
    db_person = session.get(PersonDB, person_id)
    if not db_person:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = new_details.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in update_data:
        password = update_data["password"]
        hashed_password = hash_password(password)
        extra_data["hashed_password"] = hashed_password

    if "username" in update_data:
        lowercased = update_data["username"].lower()
        extra_data["username"] = lowercased

    db_person.sqlmodel_update(update_data, update=extra_data)
    session.add(db_person)
    session.commit()
    session.refresh(db_person)
    return db_person


@course_router.delete("/delete/{course_id}")
async def delete_user(
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
