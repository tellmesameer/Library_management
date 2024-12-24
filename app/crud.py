from typing import Optional
from sqlalchemy.orm import Session
from . import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = schemas.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# Books
def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def search_books(db: Session, title: Optional[str] = None, author_name: Optional[str] = None):
    query = db.query(models.Book).join(models.Author)
    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))
    if author_name:
        query = query.filter(models.Author.author_name.ilike(f"%{author_name}%"))
    return query.all()
