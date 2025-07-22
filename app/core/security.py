from datetime import datetime, timedelta,UTC
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import status
from fastapi.exceptions import HTTPException

from app.core.config import settings

ph = PasswordHasher()
def hash_password(password: str):
    return ph.hash(password)

def verify_password(hashed: str, plain: str):
    try:
        return ph.verify(hashed, plain)
    except VerifyMismatchError:
        return False



def create_access_token(sub: str,role:str):
    data = {"sub":sub,
            "exp":(datetime.now(UTC) + timedelta(minutes=settings.jwt_exp_minutes)).timestamp(),
            "role":role}
    return jwt.encode(data, settings.rsa_private_key, algorithm=settings.jwt_algorithm)

def create_refresh_token(sub: str,role:str):
    data = {"sub": sub,
            "exp": (datetime.now(UTC) + timedelta(minutes=settings.jwt_exp_minutes)).timestamp(),
            "role": role}
    return jwt.encode(data, settings.rsa_private_key, algorithm=settings.jwt_algorithm)

def verify_token(token: str):
    try:
        token_payload = jwt.decode(token, settings.rsa_public_key, algorithms=[settings.jwt_algorithm])
        return token_payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token expired. Please refresh or log in again.")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid token")

