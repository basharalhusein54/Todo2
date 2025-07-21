from contextlib import asynccontextmanager

from fastapi import FastAPI,HTTPException

from app.core.config import settings
from app.db.database import engine, get_db
from app.api.todo import router as todos_router
from app.models.todo import Base
from app.api.auth import router as auth_router
from app.api.users import router as users_router

from app.crud import users as crud_users
from app.schemas.users import UserCreate


from fastapi import HTTPException

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = next(get_db())

    user_data = settings.superuser
    if user_data:
        try:
            crud_users.get_user_by_username(db, user_data["username"], {"sub": "admin", "role": "superuser"})
            print(f"ℹ️ Superuser '{user_data["username"]}' already exists..")
        except HTTPException as e:
            if e.status_code == 404:
                # User not found, create superuser
                crud_users.create_user(UserCreate(**user_data), db, {"sub": "admin", "role": "superuser"})
                print(f"✅ Superuser '{user_data['username']}' created.")
            else:
                # Other error, re-raise so you know something's broken
                print(f"❌ Failed to fetch superuser: {e.detail}")
                raise

    yield

app = FastAPI(lifespan=lifespan,title="ToDo API",
    description="API to manage ToDo tasks",
    version="1.0.0",
    contact={
        "name": "Bashar",
        "email": "bashar@example.com",
    })


app.include_router(todos_router)
app.include_router(users_router)
app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "main_page API"}
