from fastapi import APIRouter,  Depends, status,Path
from sqlalchemy.orm import Session
from typing import Annotated

from app.crud.auth import authorize_user
from app.db.database import get_db
from app.schemas.todo import TodoAddUpdate, TodoUpdatePartially
from app.crud import todo as crud_todo
router = APIRouter(prefix="/todos", tags=["Todos"])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[str,Depends(authorize_user)]
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(current_user:user_dependency, db:db_dependency):
    return crud_todo.read_all(db)

@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_one(todo_id:Annotated[int,Path(gt=0)], db:db_dependency):
    return  crud_todo.read_one(todo_id, db)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(todo_obj:TodoAddUpdate, db:db_dependency):
    return crud_todo.create_todo(todo_obj,db)

@router.put("/{todo_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_todo(todo_obj:TodoAddUpdate, db:db_dependency, todo_id:Annotated[int,Path(gt=0)]):
    return  crud_todo.update_todo(todo_obj,db,todo_id)

@router.patch("/{todo_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_todo(todo_obj:TodoUpdatePartially, db:db_dependency, todo_id:Annotated[int,Path(gt=0)]):
    return crud_todo.update_todo(todo_obj, db, todo_id)

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db:db_dependency, todo_id:Annotated[int,Path(gt=0)]):
    return crud_todo.delete_todo(todo_id, db)