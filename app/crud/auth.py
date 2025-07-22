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
    if not security.verify_password(user.password,login_obj.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")
    access_token = security.create_access_token(user.username,user.role)
    refresh_token = security.create_refresh_token(user.username,user.role)
    response.set_cookie("access_token", access_token,  httponly=True)
    response.set_cookie("refresh_token", refresh_token, httponly=True)
    return {"access_token": access_token, "refresh_token": refresh_token}

security_scheme = HTTPBearer()
def authorize_user(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):
    return security.verify_token(credentials.credentials)

def refresh(request,response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not refresh token log in again")
    payload = security.verify_token(refresh_token)
    access_token = security.create_access_token(payload.get("sub"),payload.get("role"))
    response.set_cookie("access_token", access_token, httponly=True)
    return {"access_token": access_token}





