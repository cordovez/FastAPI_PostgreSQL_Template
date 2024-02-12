from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from typing import Annotated
from db.database import get_db
from schemas.Item_schema import ItemSchema
from db.tables import Items

db_dependency = Annotated[Session, Depends(get_db)]
item_router = APIRouter()


@item_router.post("/create/{owner_id}")
async def create_item(item: ItemSchema, owner_id: int, db: db_dependency):
    db_item = Items(
        name=item.name, description=item.description, belongs_to_id=owner_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
