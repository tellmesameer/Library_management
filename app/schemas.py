from datetime import date
from pydantic import BaseModel
from typing import Optional 
from pydantic import BaseModel

# Author Schemas
class AuthorBase(BaseModel):
    author_name: str
    bio: Optional[str] = None
    date_of_birth: Optional[date] = None  # Use date type for proper validation and serialization

    class Config:
        orm_mode = True  # Enable ORM mode for SQLAlchemy compatibility
        json_encoders = {
            date: lambda v: v.isoformat()  # Serialize date as ISO 8601 string
        }


class AuthorCreate(AuthorBase):
    pass  # Inherits everything from AuthorBase


class Author(AuthorBase):
    author_id: int  # Add author_id for response schema

    class Config:
        orm_mode = True  # Enable ORM mode for response models


# Book Schemas
class BookBase(BaseModel):
    title: str
    author_id: int  # Foreign key linking to author
    isbn: Optional[str] = None
    published_year: Optional[int] = None
    genre: Optional[str] = None

    class Config:
        orm_mode = True  # Enable ORM mode for SQLAlchemy compatibility


class BookCreate(BookBase):
    pass  # Inherits everything from BookBase


class Book(BookBase):
    book_id: int  # Add book_id for response schema

    class Config:
        orm_mode = True  # Enable ORM mode for response models




