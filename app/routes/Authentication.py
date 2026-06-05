from sqlmodel import delete
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta
from ..dependencies import verify_user
from ..db_config import SessionDep
from ..dependencies import create_access_token
from ..tables.UserTable import UserTable
from ..settings import get_settings
from ..model.Token import Token
from pwdlib import PasswordHash
router = APIRouter(tags=["Authentication"])

password_hash = PasswordHash.recommended()
settings = get_settings()
auth = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/login")
def login(login_data: Annotated[OAuth2PasswordRequestForm,
                                Depends()],
          session: SessionDep):
    verify_user(username=login_data.username,
                password=login_data.password, session=session)
    expiry_time = timedelta(minutes=settings.access_token_expire)
    access_token = create_access_token(
        data={'sub': login_data.username}, expiry_time=expiry_time)
    return Token(access_token=access_token, token_type="bearer",
                 expiration_time=str(expiry_time))


@router.post("/sign_up")
def add_new_user(user: UserTable, session: SessionDep):
    exists = session.get(UserTable, user.username)
    if not exists:
        user.password = password_hash.hash(user.password)
        session.add(user)
        session.commit()
        session.refresh(user)
    else:
        raise HTTPException(status_code=409,
                            detail="Username already taken")
    return {"message": "Created"}
# only in dev


@router.delete("/delete_usertable")
def delete_usertable(token: Annotated[str, Depends(auth)], session: SessionDep):
    session.exec(delete(UserTable))
    session.commit()
    return {"message": "Deleted Successfully"}
