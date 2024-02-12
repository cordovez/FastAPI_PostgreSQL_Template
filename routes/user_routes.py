from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import Depends, HTTPException, APIRouter, status
from typing import Annotated
from db.database import get_db
from schemas.User_schema import UserSchema
from db.tables import Users

db_dependency = Annotated[Session, Depends(get_db)]
user_router = APIRouter()


@user_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserSchema, db: db_dependency):
    db_user = Users(username=user.username, email=user.email, is_admin=user.is_admin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return "ok"


@user_router.get("/all")
async def read_users(db: db_dependency):

    users = db.query(Users).order_by(Users.id)
    return list(users)


@user_router.get("/{user_id}")
async def read_user(user_id: int, db: db_dependency):

    return db.query(Users).filter(Users.id == user_id).first()
