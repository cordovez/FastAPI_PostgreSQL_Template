import requests
import json
from models import PersonDB, Role
from db.database import engine
from sqlmodel import Session


def get_users_data():
    response = requests.get("https://dummyjson.com/users")
    data = response.json()
    return data["users"]


def create_teachers():
    users = get_users_data()
    teachers = [teacher for teacher in users if teacher["id"] < 11]
    with Session(engine) as session:
        for teacher in teachers:
            new_teacher = PersonDB(
                email=teacher["email"],
                first_name=teacher["firstName"],
                last_name=teacher["lastName"],
                username=teacher["username"],
                role=Role.INSTRUCTOR,
            )
            session.add(new_teacher)
            session.commit()
            session.refresh(new_teacher)


def create_students():
    users = get_users_data()
    students = [student for student in users if student["id"] in range(11, 21)]

    with Session(engine) as session:
        for student in students:
            new_student = PersonDB(
                email=student["email"],
                first_name=student["firstName"],
                last_name=student["lastName"],
                username=student["username"],
                role=Role.STUDENT,
            )
            session.add(new_student)
            session.commit()
            session.refresh(new_student)


def create_staffers():
    users = get_users_data()
    staffers = [staff for staff in users if staff["id"] in range(22, 32)]
    with Session(engine) as session:
        for staff in staffers:
            new_staff = PersonDB(
                email=staff["email"],
                first_name=staff["firstName"],
                last_name=staff["lastName"],
                username=staff["username"],
                role=Role.STAFF,
            )
            session.add(new_staff)
            session.commit()
            session.refresh(new_staff)


def create_fake_db_data():
    create_staffers()
    create_students()
    create_teachers()


# if __name__ == "__main__":
#     print(create_teachers())
