from datetime import date
from typing import Optional, List
from pydantic import BaseModel, EmailStr

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

# Author Schemas
class AuthorBase(BaseModel):
    author_name: str
    bio: Optional[str] = None
    date_of_birth: Optional[date] = None

    class Config:
        from_attributes = True
        json_encoders = {
            date: lambda v: v.isoformat()
        }

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    author_id: int

    class Config:
        from_attributes = True

# Book Schemas
class BookBase(BaseModel):
    title: str
    author_id: int
    isbn: Optional[str] = None
    published_year: Optional[int] = None
    genre: Optional[str] = None

    class Config:
        from_attributes = True

class BookCreate(BookBase):
    pass

class Book(BookBase):
    book_id: int

    class Config:
        from_attributes = True

# User Schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

# Authentication Schemas
class LoginRequest(BaseModel):
    username: str
    password: str

# Paginated Books Schema (if needed)
class PaginatedBooks(BaseModel):
    total: int
    page: int
    per_page: int
    books: List[Book]

    class Config:
        from_attributes = True
