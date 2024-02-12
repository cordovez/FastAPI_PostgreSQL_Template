import uvicorn
from fastapi import FastAPI

from db.database import engine, DBBase
from routes.user_routes import user_router
from routes.item_routes import item_router

app = FastAPI()

DBBase.metadata.create_all(bind=engine)

app.include_router(user_router, tags=["Users"], prefix="/users")
app.include_router(item_router, tags=["Items"], prefix="/items")


def main():
    uvicorn.run(reload=True, app="main:app")


if __name__ == "__main__":
    main()
