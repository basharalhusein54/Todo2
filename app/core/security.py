from datetime import datetime, timedelta,UTC
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from passlib.context import CryptContext
from starlette import status
from starlette.exceptions import HTTPException

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)


private_key = settings.rsa_private_key
public_key = settings.rsa_public_key

def create_access_token(sub: str):
    data = {"sub":sub,
            "exp":(datetime.now(UTC) + timedelta(minutes=settings.jwt_exp_minutes)).timestamp()}
    return jwt.encode(data, private_key, algorithm=settings.jwt_algorithm)

def create_refresh_token(sub: str):
    data = {"sub":sub,
            "exp":(datetime.now(UTC) + timedelta(minutes=settings.jwt_exp_days)).timestamp()}
    return jwt.encode(data, private_key, algorithm=settings.jwt_algorithm)

def verify_token(token: str):
    try:
        token_payload = jwt.decode(token, public_key, algorithms=[settings.jwt_algorithm])
        return token_payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token expired. Please refresh or log in again.")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid token")

