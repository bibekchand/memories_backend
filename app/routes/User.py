from fastapi import APIRouter, Depends
from typing import Annotated
from ..db_config import SessionDep
from ..dependencies import verify_token
from ..tables.UserTable import UserTable
from fastapi.security import OAuth2PasswordBearer
from ..model.User import User


router = APIRouter(tags=["User"])
auth = OAuth2PasswordBearer(tokenUrl="login")


@router.get("/user", response_model=User)
def get_user_info(token: Annotated[str, Depends(auth)], session: SessionDep):
    username = verify_token(token, session)
    user = session.get(UserTable, username)
    return user