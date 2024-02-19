from fastapi import Depends, HTTPException, APIRouter, status, Query
from db.database import engine
from models import Book, BookUpdate
from sqlmodel import select, Session

book_router = APIRouter()

session = Session(engine)


@book_router.get("/", response_model=list[Book], status_code=status.HTTP_200_OK)
async def get_all_books(offset: int = 0, limit: int = Query(default=100, le=100)):
    with session:
        return session.exec(select(Book).offset(offset).limit(limit)).all()


@book_router.get("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_one_book(book_id: int):
    with session:
        if book := session.get(Book, book_id):
            return book
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@book_router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_a_book(new_book: Book) -> Book:
    new_book = Book(
        author=new_book.author, title=new_book.title, description=new_book.description
    )
    with session:
        session.add(new_book)
        session.commit()
        session.refresh(new_book)
        return new_book


@book_router.patch("/{book_id}", response_model=Book)
async def update_a_book(book_id: int, new_details: BookUpdate) -> Book:
    with session:
        db_book = session.get(Book, book_id)
        if not db_book:
            raise HTTPException(status_code=404, detail="Book not found")

        update_data = new_details.model_dump(exclude_unset=True)
        db_book.sqlmodel_update(update_data)
        session.add(db_book)
        session.commit()
        session.refresh(db_book)
        return db_book


@book_router.delete("/{book_id}")
async def delete_book(book_id: int):
    with session:
        book = session.get(Book, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Hero not found")
        session.delete(book)
        session.commit()
        return {"deleted": True}
