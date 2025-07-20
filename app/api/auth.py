from fastapi import APIRouter,Depends
from fastapi.responses import Response
from fastapi.requests import Request
from typing import Annotated

from sqlalchemy.orm import Session
from starlette import status

from app.schemas.auth import Login
from app.db.database import get_db
from app.crud import auth as crud_auth
router = APIRouter(prefix="/auth", tags=["Authentication"])

db_dependency = Annotated[Session,Depends(get_db)]
@router.post("/login",status_code=status.HTTP_200_OK)
async def auth(login_obj:Login,db:db_dependency,response:Response):
    return crud_auth.authenticate_user(login_obj,db,response)

@router.post("/refresh",status_code=status.HTTP_200_OK)
async def refresh_token(request:Request, response:Response):
    return crud_auth.refresh(request,response)

