from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from .database import engine, Base
from app.routers import users, auth, books, authors

app = FastAPI()

# Drop all tables and recreate them
Base.metadata.create_all(bind=engine)

# Include Routers
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(books.router)
app.include_router(authors.router)


# Add custom OpenAPI schema to include Bearer Token
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Library Management API",
        version="1.0.0",
        description="This is a Library Management API that uses Bearer Token Authentication.",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
