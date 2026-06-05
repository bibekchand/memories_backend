import jwt
from datetime import datetime, timedelta, timezone
from .tables.UserTable import UserTable
from pwdlib import PasswordHash
from fastapi import HTTPException
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from .settings import get_settings
from .db_config import SessionDep

password_hash = PasswordHash.recommended()
settings = get_settings()


def verify_token(token: str, session: SessionDep):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token,
                             settings.secret_key, algorithms=[
                                 settings.algorithm])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401, detail="Token expired. Please login again")
    return username


def verify_user(username: str, password: str, session: SessionDep):
    credentials_error = HTTPException(
        status_code=401,
        detail="Invalid username or password"
    )
    user = session.get(UserTable, username)
    if not user:
        raise credentials_error
    if not password_hash.verify(password, user.password):
        raise credentials_error


def create_access_token(data: dict, expiry_time: timedelta | None = None):
    to_encode = data.copy()
    if expiry_time:
        expire = datetime.now(timezone.utc) + expiry_time
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt
