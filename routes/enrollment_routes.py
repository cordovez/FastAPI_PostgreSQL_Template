from fastapi import Depends, HTTPException, APIRouter, status, Query, Body
from db.database import engine
from models import EnrollmentCreate, EnrollmentDB, EnrollmentRead, EnrollmentUpdate
from sqlmodel import select, Session
from datetime import date
from typing import Annotated
from pydantic import BaseModel

enrollment_router = APIRouter()


def get_session():
    with Session(engine) as session:
        yield session


today = date.today()


@enrollment_router.get("/", response_model=list[EnrollmentRead])
async def get_all_enrollments(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    return session.exec(select(EnrollmentDB).offset(offset).limit(limit)).all()


@enrollment_router.post(
    "/", response_model=EnrollmentRead, status_code=status.HTTP_201_CREATED
)
async def enroll_student(
    *,
    session: Session = Depends(get_session),
    new_enrollment: EnrollmentCreate,
):
    db_enrollment = EnrollmentDB.model_validate(new_enrollment)
    session.add(db_enrollment)
    session.commit()
    session.refresh(db_enrollment)
    return db_enrollment


@enrollment_router.get("/{student_id}/", response_model=EnrollmentRead)
async def get_student_enrollment(
    *,
    session: Session = Depends(get_session),
    student_id: int,
):
    if db_enrollment := session.exec(
        select(EnrollmentDB).where(EnrollmentDB.student_id == student_id)
    ):
        for student in db_enrollment:
            return student
    else:
        raise HTTPException(status_code=404, detail="Student not found")


@enrollment_router.patch("/{enrollment_id}", response_model=EnrollmentRead)
async def update_an_enrollment(
    *,
    session: Session = Depends(get_session),
    enrollment_id: int,
    new_details: EnrollmentUpdate,
):
    db_enrollment = session.get(EnrollmentDB, enrollment_id)
    if not db_enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    update_data = new_details.model_dump(exclude_unset=True)

    db_enrollment.sqlmodel_update(update_data)
    session.add(db_enrollment)
    session.commit()
    session.refresh(db_enrollment)
    return db_enrollment


@enrollment_router.delete(
    "/{enrollment_id}",
    response_model=bool,
    response_description='"true" if successful',
)
async def delete_enrollment(
    *, session: Session = Depends(get_session), enrollment_id: int
):
    enrollment = session.get(EnrollmentDB, enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    session.delete(enrollment)
    session.commit()

    return True
