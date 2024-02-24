import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from db.database import engine
from routes.user_routes import user_router
from routes.course_routes import course_router
from routes.enrollment_routes import enrollment_router
from sqlmodel import SQLModel
from fake_data import create_fake_db_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    create_fake_db_data()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(user_router, tags=["Users"], prefix="/users")
app.include_router(course_router, tags=["Courses"], prefix="/courses")
app.include_router(enrollment_router, tags=["Enrollment"], prefix="/enrollment")


def main():
    uvicorn.run(reload=True, app="main:app")


if __name__ == "__main__":
    main()
