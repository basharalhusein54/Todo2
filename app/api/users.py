from fastapi import APIRouter, Depends,status
from sqlalchemy.orm import Session
from typing import Annotated

from app.db.database import get_db
from app.crud import users as crud_users
from app.schemas.users import UsersAdd
router = APIRouter(prefix="/users", tags=["Users"])

db_dependency = Annotated[Session,Depends(get_db)]
@router.get("/", status_code=status.HTTP_200_OK)
async def get_users(db:db_dependency):
    return crud_users.read_all(db)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user_obj:UsersAdd,db:db_dependency):
    return crud_users.create_user(user_obj,db)