from fastapi import Depends, HTTPException, APIRouter, status, Query
from db.database import engine
from models import EnrollmentCreate, EnrollmentDB, EnrollmentRead, Levels
from sqlmodel import select, Session
from datetime import date

enrollment_router = APIRouter()


def get_session():
    with Session(engine) as session:
        yield session


today = date.today()


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
