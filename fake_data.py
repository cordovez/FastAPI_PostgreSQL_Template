import requests
from models import PersonDB, Role, Subject, CourseDB
from db.database import engine
from sqlmodel import Session


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


def create_fake_courses():
    with Session(engine) as session:
        for language in list(Subject):
            new_course = CourseDB(course_name=language.value)
            session.add(new_course)
            session.commit()
            session.refresh(new_course)


create_fake_users()
create_fake_courses()
