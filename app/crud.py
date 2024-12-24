from sqlalchemy.orm import Session
from . import models, schemas
from typing import Optional 
# Author CRUD
def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_authors(db: Session):
    return db.query(models.Author).all()

# Book CRUD
def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db: Session):
    return db.query(models.Book).all()

# Update Book
def update_book(db: Session, book_id: int, book_update: schemas.BookCreate):
    db_book = db.query(models.Book).filter(models.Book.book_id == book_id).first()
    if not db_book:
        return None
    for key, value in book_update.dict().items():
        if value is not None:  # Update only non-null fields
            setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

# Delete Book
def delete_book(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.book_id == book_id).first()
    if not db_book:
        return None
    db.delete(db_book)
    db.commit()
    return db_book

# Delete Author
def delete_author(db: Session, author_id: int):
    db_author = db.query(models.Author).filter(models.Author.author_id == author_id).first()
    if not db_author:
        return None
    db.delete(db_author)
    db.commit()
    return db_author

from sqlalchemy.orm import Session
from sqlalchemy import or_

# Search Books by Title or Author Name
def search_books(db: Session, title: Optional[str] = None, author_name: Optional[str] = None):
    query = db.query(models.Book).join(models.Author, models.Book.author_id == models.Author.author_id)

    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))
    
    if author_name:
        query = query.filter(models.Author.author_name.ilike(f"%{author_name}%"))
    
    return query.all()
