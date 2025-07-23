from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated

from app.crud.auth import authorize_user
from app.db.database import get_db
from app.crud import users as crud_users
from app.schemas.users import UserCreate, ChangePasswordSchema

router = APIRouter(prefix="/users", tags=["Users"])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(authorize_user)]


@router.get("/get_users", status_code=status.HTTP_200_OK)
async def get_users(db: db_dependency, current_user: user_dependency):
    return crud_users.get_users(db, current_user)

@router.get("/get_user_byusername/{username}", status_code=status.HTTP_200_OK)
async def get_user(db: db_dependency, username: str, current_user: user_dependency):
    return  crud_users.get_user_by_username(db, username, current_user)

@router.get("/get_user_byid/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(db: db_dependency, user_id: int, current_user: user_dependency):
    return  crud_users.get_user_by_id(db, user_id, current_user)

@router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(user_obj: UserCreate, db: db_dependency, current_user: user_dependency):
    return crud_users.create_user(user_obj, db, current_user)

@router.delete("/delete_user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(db: db_dependency, user_id: int, current_user: user_dependency):
    return crud_users.delete_user(db, user_id, current_user)

@router.patch("/change_password/", status_code=status.HTTP_200_OK)
async def change_password(db: db_dependency,
                      change_password_schema: ChangePasswordSchema,
                      current_user: user_dependency):
    return crud_users.change_password(db,change_password_schema,current_user)
