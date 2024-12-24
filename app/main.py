from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas, crud
from .database import engine, Base, get_db
from .auth import (
    authenticate_user,
    create_access_token,
    get_active_user,
    create_user
)

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Public Endpoints
@app.post("/users/", response_model=schemas.UserResponse)
def create_user_endpoint(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db=db, user=user)

@app.post("/token")
def login(form_data: schemas.LoginRequest):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/books/", response_model=schemas.PaginatedBooks)
def get_books(
    db: Session = Depends(get_db),
    title: Optional[str] = Query(None),
    author_name: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 10
):
    books = crud.search_books(db=db, title=title, author_name=author_name, skip=skip, limit=limit)
    total = crud.get_books_count(db=db, title=title, author_name=author_name)
    return {"books": books, "total": total}

# Protected Endpoints
@app.post("/books/", response_model=schemas.Book, dependencies=[Depends(get_active_user)])
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)

@app.put("/books/{book_id}", response_model=schemas.Book, dependencies=[Depends(get_active_user)])
def update_book(book_id: int, book_update: schemas.BookCreate, db: Session = Depends(get_db)):
    updated_book = crud.update_book(db=db, book_id=book_id, book_update=book_update)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book

@app.delete("/books/{book_id}", dependencies=[Depends(get_active_user)])
def delete_book(book_id: int, db: Session = Depends(get_db)):
    deleted_book = crud.delete_book(db=db, book_id=book_id)
    if not deleted_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}

@app.post("/authors/", response_model=schemas.Author, dependencies=[Depends(get_active_user)])
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)

@app.put("/authors/{author_id}", dependencies=[Depends(get_active_user)])
def update_author(author_id: int, author_update: schemas.AuthorCreate, db: Session = Depends(get_db)):
    updated_author = crud.update_author(db=db, author_id=author_id, author_update=author_update)
    if not updated_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return updated_author

@app.delete("/authors/{author_id}", dependencies=[Depends(get_active_user)])
def delete_author(author_id: int, db: Session = Depends(get_db)):
    deleted_author = crud.delete_author(db=db, author_id=author_id)
    if not deleted_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return {"message": "Author deleted successfully"}
