import requests
from models import (
    PersonDB,
    Role,
    Subject,
    CourseDB,
    EnrollmentCreate,
    EnrollmentDB,
    StudentDB,
    PersonCreate,
    StudentEnrollment,
    Levels,
)
from db.database import engine
from sqlmodel import Session, select
import random


def get_users_data():
    response = requests.get("https://dummyjson.com/users?limit=100")
    data = response.json()
    return data["users"]


def assign_role_based_on_id(user_id):
    match user_id:
        case user_id if user_id < 11:
            return Role.STUDENT
        case user_id if 11 <= user_id < 21:
            return Role.INSTRUCTOR
        case user_id if 21 <= user_id < 31:
            return Role.STAFF
        case user_id if 31 <= user_id < 41:
            return Role.TECH_ADMIN
        case user_id if 41 <= user_id < 51:
            return Role.ACADEMIC_ADMIN
        case _:
            return "not assigned"


def create_fake_users():
    fake_data = get_users_data()
    list_of_users = []
    with Session(engine) as session:
        for user in fake_data:
            if user["id"] < 52:
                new_user = PersonDB(
                    email=user["email"],
                    first_name=user["firstName"],
                    last_name=user["lastName"],
                    username=user["username"],
                    role=assign_role_based_on_id(user["id"]),
                    street_address=user["address"].get("address", None),
                    locality=user["address"].get("city", None),
                    post_code=user["address"].get("postalCode", None),
                    country="United States of America",
                    password_hashed=user["password"],
                )

                session.add(new_user)
                session.commit()
                session.refresh(new_user)

                list_of_users.append(new_user)
    return list_of_users


def create_fake_courses():
    with Session(engine) as session:
        for language in list(Subject):
            new_course = CourseDB(course_name=language.value)
            session.add(new_course)
            session.commit()
            session.refresh(new_course)


def create_fake_students():
    with Session(engine) as session:
        users = session.exec(select(PersonDB)).all()
        for user in users:
            if user.role == "student":
                new_student = StudentDB(
                    username=user.username,
                    email=user.email,
                    first_name=user.first_name,
                    last_name=user.last_name,
                )
                session.add(new_student)
                session.commit()
                session.refresh(new_student)


def select_a_course():
    with Session(engine) as session:
        courses = session.exec(select(CourseDB)).all()
        return random.choice(courses)


def create_fake_enrollments():
    with Session(engine) as session:
        students = session.exec(select(StudentDB)).all()
        for student in students:
            random_course = select_a_course()
            new_enrollment = EnrollmentDB(
                student_id=student.id,
                course_id=random_course.id,
                course_name=random_course.course_name,
                instructor_id=random.choice(list(range(11, 21))),
                start_level=random.choice(["a1", "a2", "b1", "b2", "c1", "c2"]),
            )

            student.sqlmodel_update({"enrollments": [new_enrollment.id]})

            session.add(student)
            session.add(new_enrollment)
            session.commit()
            session.refresh(student)
            session.refresh(new_enrollment)


def create_join_of_fake_data():
    with Session(engine) as session:
        enrollments = session.exec(select(EnrollmentDB)).all()

        for enroll in enrollments:
            join = StudentEnrollment(
                enrollment_id=enroll.id, student_id=enroll.student_id
            )

            session.add(join)
            session.commit()
            session.refresh(join)


def main():
    create_fake_users()
    create_fake_courses()
    create_fake_students()
    create_fake_enrollments()
    create_join_of_fake_data()


if __name__ == "__main__":
    main()
