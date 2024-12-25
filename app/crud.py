from sqlalchemy.orm import Session
from typing import Optional
from . import models, schemas


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = schemas.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return schemas.UserResponse(id=db_user.id, username=db_user.username, email=db_user.email)


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def search_books(db: Session, title: Optional[str] = None, author_name: Optional[str] = None, skip: int = 0, limit: int = 10):
    query = db.query(models.Book).join(models.Author)
    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))
    if author_name:
        query = query.filter(models.Author.author_name.ilike(f"%{author_name}%"))
    return query.offset(skip).limit(limit).all()
