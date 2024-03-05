from fastapi import Depends, HTTPException, APIRouter, status, Query
from db.database import engine
from models import (
    CourseRead,
    PersonCreate,
    PersonRead,
    PersonUpdate,
    PersonDB,
    PersonUpdateRole,
    Role,
)
from sqlmodel import select, Session

user_router = APIRouter()


def get_session():
    with Session(engine) as session:
        yield session


def create_default_username(fname, lname):
    return (fname[0] + lname[:7]).lower()


def hash_password(password: str) -> str:
    return f"faked {password} goes here"


@user_router.get("/", response_model=list[PersonRead], status_code=status.HTTP_200_OK)
async def get_all_users(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    return session.exec(select(PersonDB).offset(offset).limit(limit)).all()


@user_router.post("/", response_model=PersonRead, status_code=status.HTTP_201_CREATED)
async def create_a_user(
    *,
    session: Session = Depends(get_session),
    new_person: PersonCreate,
):
    # TO DO: add students to student db
    hashed_password = hash_password(new_person.password)

    extra_data = {
        "password_hashed": hashed_password,
        "username": create_default_username(
            new_person.first_name, new_person.last_name
        ),
    }
    db_person = PersonDB.model_validate(new_person, update=extra_data)
    session.add(db_person)
    session.commit()
    session.refresh(db_person)
    return db_person


@user_router.get(
    "/by-role", response_model=list[PersonRead], status_code=status.HTTP_200_OK
)
async def get_users_by_role(
    *,
    session: Session = Depends(get_session),
    role: Role,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    # return role
    return session.exec(
        select(PersonDB).where(PersonDB.role == role).offset(offset).limit(limit)
    )


@user_router.get(
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


@user_router.get(
    "/{student_id}/course",
    description="Student's Course",
    response_model=CourseRead,
    status_code=status.HTTP_200_OK,
)
async def get_student_course(
    *,
    session: Session = Depends(get_session),
    student_id: int,
):
    if student := session.get(PersonDB, student_id):
        return student.course
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@user_router.patch("/{person_id}", response_model=PersonRead)
async def update_a_user(
    *,
    session: Session = Depends(get_session),
    person_id: int,
    new_details: PersonUpdate,
):
    db_person = session.get(PersonDB, person_id)
    if not db_person:
        raise HTTPException(status_code=404, detail="Person not found")

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


@user_router.patch("/{person_id}/role", response_model=PersonRead)
async def change_role(
    *,
    session: Session = Depends(get_session),
    person_id: int,
    new_details: PersonUpdateRole,
):
    """
    This route is different from regular update, in that it would be accessible only to TECH_ADMIN to change a user's status,
    """
    db_person = session.get(PersonDB, person_id)
    if not db_person:
        raise HTTPException(status_code=404, detail="Person not found")

    update_data = new_details.model_dump(exclude_unset=True)

    db_person.sqlmodel_update(update_data)
    session.add(db_person)
    session.commit()
    session.refresh(db_person)
    return db_person


@user_router.delete(
    "/{person_id}",
    response_model=bool,
    response_description='"true" if successful',
)
async def delete_user(
    *,
    session: Session = Depends(get_session),
    person_id: int,
):
    person = session.get(PersonDB, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    session.delete(person)
    session.commit()
    return True
