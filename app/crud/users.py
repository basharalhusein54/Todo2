from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from fastapi.exceptions import HTTPException
from fastapi import status

from app.models.users import Users
from app.core.security import hash_password,verify_password
from app.schemas.users import UserShow

def check_ability(current_user):
    if current_user.get("role") != "superuser":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Only superuser is allowed")

def get_users(db, current_user):
    check_ability(current_user)
    results = db.query(Users).all()
    if results:
        return results
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)


def get_user_by_username(db, username,current_user):
    check_ability(current_user)
    results = db.query(Users).filter(Users.username == username).first()
    if results:
        return UserShow.model_validate(results)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found")

def get_user_by_id(db, user_id:int,current_user):
    check_ability(current_user)
    results = db.query(Users).filter(Users.id == user_id).first()
    if results:
        return UserShow.model_validate(results)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found")

def create_user(user_obj, db, current_user):
    check_ability(current_user)
    user_obj.password = hash_password(user_obj.password)
    user_obj = Users(**user_obj.model_dump())
    db.add(user_obj)
    try:
        db.commit()
        db.refresh(user_obj)
        return UserShow.model_validate(user_obj)
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=str(e.__cause__) if e.__cause__ else str(e))
    except OperationalError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Database is unreachable.")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(e.__cause__) if e.__cause__ else str(e))

def delete_user(db, user_id:int,current_user):
    check_ability(current_user)
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    try:
        db.delete(user)
        db.commit()
    except OperationalError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Database is unreachable.")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(e.__cause__) if e.__cause__ else str(e))

def change_password(db,data,current_user):
    check_ability(current_user)
    if data.username:
        user = db.query(Users).filter(Users.username == data.username).first()
    elif data.email:
        user = db.query(Users).filter(Users.email == data.email).first()
    else:
        raise HTTPException(status_code=400, detail="Username or email required")

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, data.old_password):
        raise HTTPException(status_code=401, detail="Old password is incorrect")

    user.password = hash_password(data.new_password)
    try:
        db.commit()
    except OperationalError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Database is unreachable.")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(e.__cause__) if e.__cause__ else str(e))
    return {"message": "Password changed successfully"}