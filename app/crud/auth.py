from fastapi import status, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core import security
from app.models.users import  Users

def authenticate_user(login_obj,db,response):
    user = db.query(Users).filter(Users.username == login_obj.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    if not security.verify_password(login_obj.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")
    access_token = security.create_access_token(login_obj.username)
    refresh_token = security.create_refresh_token(login_obj.username)
    response.set_cookie("access_token", access_token,  httponly=True)
    response.set_cookie("refresh_token", refresh_token, httponly=True)
    return {"access_token": access_token, "refresh_token": refresh_token}

security_scheme = HTTPBearer()
def authorize_user(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):
    token_payload = security.verify_token(credentials.credentials)
    print(token_payload)
    return token_payload.get('sub')

def refresh(request,response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not refresh token log in again")
    payload = security.verify_token(refresh_token)
    access_token = security.create_access_token(payload.get("sub"))
    response.set_cookie("access_token", access_token, httponly=True)
    return {"access_token": access_token}




