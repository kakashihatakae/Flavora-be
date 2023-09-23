from datetime import timedelta, datetime
from typing import Union
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    data: dict,
    SECRET_KEY: str,
    ALGORITHM: str,
    expires_delta: Union[timedelta, None] = None,
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(user_password: str, db_password: str):
    return pwd_context.verify(user_password, db_password)


def get_hashed_password(user_password: str):
    return pwd_context.hash(user_password)
