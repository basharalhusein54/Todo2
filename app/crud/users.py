from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError, OperationalError,SQLAlchemyError
from fastapi.exceptions import HTTPException
from fastapi import status
from app.models.users import Users
from app.schemas.users import UsersAdd
from app.core.security import hash_password

def read_all(db):
    results = db.query(Users).all()
    if results:
        return results
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,)

def create_user(user_obj,db):
    user_obj.password = hash_password(user_obj.password)
    user_obj = Users(**user_obj.model_dump())
    db.add(user_obj)
    try:
        db.commit()
        db.refresh(user_obj)
        return {"username": user_obj.username,"email":user_obj.email}
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
