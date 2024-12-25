from fastapi import FastAPI
from .database import engine, Base
from app.routers import users, auth, books, authors


app = FastAPI()

# Drop all tables and recreate them
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Include Routers
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(books.router)
app.include_router(authors.router)
