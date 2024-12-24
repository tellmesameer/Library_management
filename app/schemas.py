from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr
from typing import List

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


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str  # Add other fields as needed

    class Config:
        orm_mode = True  # This allows SQLAlchemy models to be automatically converted to Pydantic models


class LoginRequest(BaseModel):
    username: str
    password: str

class PaginatedBooks(BaseModel):
    total: int  # Total number of books in the database
    page: int  # Current page number
    per_page: int  # Number of books per page
    books: List[Book]  # List of books on the current page

    class Config:
        orm_mode = True  # This allows SQLAlchemy models to be automatically converted to Pydantic models
