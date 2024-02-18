import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from db.database import engine
from routes.user_routes import user_router
from sqlmodel import SQLModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(user_router, tags=["Users"], prefix="/users")


def main():
    uvicorn.run(reload=True, app="main:app")


if __name__ == "__main__":
    main()
