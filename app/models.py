from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base


class Author(Base):
    __tablename__ = "author"
    author_id = Column(Integer, primary_key=True, index=True)
    author_name = Column(String(255), nullable=False)
    bio = Column(String(1000), nullable=True)
    date_of_birth = Column(Date, nullable=True)


class Book(Base):
    __tablename__ = "books"
    book_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author_id = Column(Integer, ForeignKey("author.author_id"), nullable=False)
    isbn = Column(String(13), nullable=True)
    published_year = Column(Integer, nullable=True)
    genre = Column(String(50), nullable=True)
    author = relationship("Author")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
