import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from db.database import engine
from routes.user_routes import user_router
from routes.course_routes import course_router
from sqlmodel import SQLModel

# import models


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(user_router, tags=["Users"], prefix="/users")
app.include_router(course_router, tags=["Courses"], prefix="/courses")


def main():
    uvicorn.run(reload=True, app="main:app")


if __name__ == "__main__":
    main()
