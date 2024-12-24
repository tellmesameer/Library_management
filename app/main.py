from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas, crud
from .database import engine, Base, get_db
from fastapi.security import OAuth2PasswordRequestForm
from .auth import (
    authenticate_user,
    create_access_token,
    get_active_user,
)

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Public Endpoints
@app.get("/books/", response_model=List[schemas.Book])
def search_books_endpoint(
    title: Optional[str] = Query(None, description="Search by book title"),
    author_name: Optional[str] = Query(None, description="Search by author name"),
    db: Session = Depends(get_db)
):
    books = crud.search_books(db=db, title=title, author_name=author_name)
    return books

@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(db: Session = Depends(get_db)):
    return crud.get_authors(db=db)

# Authentication Endpoint
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

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
