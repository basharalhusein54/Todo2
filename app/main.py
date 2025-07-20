from fastapi import FastAPI
from app.db.database import engine
from app.api.todo import router as todos_router
from app.models.todo import Base
from app.api.auth import router as auth_router
from app.api.users import router as users_router
app = FastAPI(title="ToDo API",
    description="API to manage ToDo tasks",
    version="1.0.0",
    contact={
        "name": "Bashar",
        "email": "bashar@example.com",
    })
Base.metadata.create_all(engine)

app.include_router(todos_router)
app.include_router(users_router)
app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "mainpage"}
