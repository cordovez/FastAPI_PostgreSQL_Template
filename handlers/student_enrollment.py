from models import EnrollmentDB, EnrollmentCreate, EnrollmentRead, PersonDB
from fastapi import HTTPException
from typing import Annotated
from sqlmodel import Session


async def create_enrollment(
    session: Session,
    enrollment_data: EnrollmentCreate,
) -> EnrollmentRead:

    db_enrollment = EnrollmentDB.model_validate(enrollment_data)
    session.add(db_enrollment)
    session.commit()
    session.refresh(db_enrollment)
    return db_enrollment


async def add_course_to_student(student_id, enrollment, session):
    """Function finds person and verifies the role is "student" """
    course_id = enrollment.course_id
    if person := session.get(PersonDB, student_id):
        if person.role == "student":

            update_data = {"course_id": course_id}

            person.sqlmodel_update(update_data)
            session.add(person)
            session.commit()
            session.refresh(person)
        else:
            raise HTTPException(status_code=404, detail="Person not found")


async def enroll_student(session, enrollment_data):
    new_enrollment = await create_enrollment(session, enrollment_data)
    await add_course_to_student(new_enrollment.student_id, new_enrollment, session)
    return new_enrollment
