from sqlmodel import Session, select

# from sqlalchemy import select
from fastapi import Depends, HTTPException, APIRouter, status

# from typing import Annotated
from db.database import engine

user_router = APIRouter()


@user_router.post(
    "/add",
)
async def add_person(person):
    pass


@user_router.post("/contact-info-update/{userid}")
async def update_contact_info():
    pass
