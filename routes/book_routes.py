from fastapi import Depends, HTTPException, APIRouter, status, Query
from db.database import engine
from models import Book, BookUpdate, BookCreate, BookRead
from sqlmodel import select, Session

book_router = APIRouter()


def get_session():
    with Session(engine) as session:
        yield session


def hash_password(password: str) -> str:
    return f"faked {password} goes here"


@book_router.get("/", response_model=list[BookRead], status_code=status.HTTP_200_OK)
async def get_all_books(
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    session: Session = Depends(get_session),
):
    with session:
        return session.exec(select(Book).offset(offset).limit(limit)).all()


@book_router.get("/{book_id}", response_model=BookRead, status_code=status.HTTP_200_OK)
async def get_one_book(
    book_id: int,
    session: Session = Depends(get_session),
):
    with session:
        if book := session.get(Book, book_id):
            return book
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@book_router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_a_book(
    new_book: BookCreate,
    session: Session = Depends(get_session),
):
    hashed_password = hash_password(new_book.password)
    # new_book = Book(
    #     author=new_book.author, title=new_book.title, description=new_book.description
    # )
    with session:
        extra_data = {"hashed_password": hashed_password}
        db_book = Book.model_validate(new_book, update=extra_data)
        session.add(db_book)
        session.commit()
        session.refresh(db_book)
        return db_book


@book_router.patch("/{book_id}", response_model=BookRead)
async def update_a_book(
    book_id: int, new_details: BookUpdate, session: Session = Depends(get_session)
) -> Book:
    with session:
        db_book = session.get(Book, book_id)
        if not db_book:
            raise HTTPException(status_code=404, detail="Book not found")

        update_data = new_details.model_dump(exclude_unset=True)
        extra_data = {}
        if "password" in update_data:
            password = update_data["password"]
            hashed_password = hash_password(password)
            extra_data["hashed_password"] = hashed_password

        db_book.sqlmodel_update(update_data, update=extra_data)
        session.add(db_book)
        session.commit()
        session.refresh(db_book)
        return db_book


@book_router.delete("/{book_id}")
async def delete_book(book_id: int, session: Session = Depends(get_session)):
    with session:
        book = session.get(Book, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        session.delete(book)
        session.commit()
        return {"deleted": True}
