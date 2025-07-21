from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from fastapi.exceptions import HTTPException
from fastapi import status

from app.models.users import Users
from app.core.security import hash_password


def get_users(db, current_user):
    if current_user.get("role") != "superuser":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Only superuser is allowed")
    results = db.query(Users).all()
    if results:
        return results
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)


def get_user_by_username(db, username,current_user):
    if current_user.get("role") != "superuser":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Only superuser is allowed")
    results = db.query(Users).filter(Users.username == username).first()
    if results:
        return results
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found")

def create_user(user_obj, db, current_user):
    if current_user.get("role") != "superuser":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Only superuser is allowed")
    user_obj.password = hash_password(user_obj.password)
    user_obj = Users(**user_obj.model_dump())
    db.add(user_obj)
    try:
        db.commit()
        db.refresh(user_obj)
        return {"username": user_obj.username, "email": user_obj.email}
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


