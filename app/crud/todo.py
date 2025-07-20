from app.models.todo import Todos
from fastapi.exceptions import HTTPException
from fastapi import status
def read_all(db):
    return db.query(Todos).all()

def read_one(todo_id, db):
    result = db.query(Todos).filter(Todos.id == todo_id).first()
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Todo with ID {todo_id} not found")
    return result

def create_todo(todo_obj,db):
    new_todo = Todos(**todo_obj.model_dump())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

def update_todo(todo_obj, db, todo_id):
    existing_todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if existing_todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Todo with ID {todo_id} not found")
    changes=0
    for field,value in todo_obj.model_dump().items():
        if getattr(existing_todo,field) != value:
            setattr(existing_todo,field,value)
            changes += 1
    if changes == 0:
        return {"message": "Nothing to update"}
    db.commit()
    db.refresh(existing_todo)
    return  {"message": "todo updated successfully"}

def delete_todo(todo_id, db):
    existing_todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if existing_todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Todo with ID {todo_id} not found")
    db.delete(existing_todo)
    db.commit()
