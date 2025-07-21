from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated

from app.crud.auth import authorize_user
from app.db.database import get_db
from app.crud import users as crud_users
from app.schemas.users import UserCreate

router = APIRouter(prefix="/users", tags=["Users"])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(authorize_user)]


@router.get("/get_users", status_code=status.HTTP_200_OK)
async def get_users(db: db_dependency, current_user: user_dependency):
    return crud_users.get_users(db, current_user)


@router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(user_obj: UserCreate, db: db_dependency, current_user: user_dependency):
    return crud_users.create_user(user_obj, db, current_user)
