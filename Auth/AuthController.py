from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from Auth.AuthSchemas import UserSchema
from Auth.utils import create_access_token, verify_password, get_hashed_password
from Auth import CRUD
from Models.User import User

from database import SessionLocal, engine

from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
import time
from typing import Annotated
from jose import jwt, JWTError

AuthRouter = APIRouter()
# -----
# TODO: please change
SECRET_KEY = "Shreyas"
# ----
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_MINUTES = 60 * 24 * 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def authenticate_request(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if "email" not in payload:
            raise credentials_exception

        email: str = payload["email"]
        expiration: int = payload["expiry"]
        role: str = payload["role"]
        if time.mktime(datetime.utcnow().timetuple()) > expiration:
            raise credentials_exception

    except JWTError:
        raise credentials_exception
    user = CRUD.get_user_by_email(email=email, role=role, db=db)

    if not user:
        raise credentials_exception
    return user


# @AuthRouter.get("/init_trip")
# async def basic(k: Annotated[str, Depends(authenticate_request)]):
#     print(k)
#     return ""


@AuthRouter.post("/register")
async def register(user: UserSchema, db: Session = Depends(get_db)):
    hashed_password = get_hashed_password(user.password)
    user_hashed = User(email=user.email, password=hashed_password, role=user.role)
    try:
        CRUD.create_user(user=user_hashed, db=db)
    except SQLAlchemyError as e:
        db.rollback()
        # TODO: change statues code
        raise HTTPException(status_code=404, detail=f"User already present. Error: {e}")
    accessTokenExpiry = timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
    tokenExpiry = accessTokenExpiry + datetime.utcnow()
    tokenExpiryUnixTime = time.mktime(tokenExpiry.timetuple())
    accessToken = create_access_token(
        data={"email": user.email, "expiry": tokenExpiryUnixTime, "role": user.role},
        SECRET_KEY=SECRET_KEY,
        ALGORITHM=ALGORITHM,
        expires_delta=accessTokenExpiry,
    )

    return {"token": accessToken, "expiry": int(tokenExpiryUnixTime)}


@AuthRouter.post("/login")
async def login(user: UserSchema, db: Session = Depends(get_db)):
    try:
        current_user = CRUD.get_user_by_email(email=user.email, role=user.role, db=db)
    except SQLAlchemyError as e:
        # TODO: change status code
        raise HTTPException(status_code=404, detail="Singin DB error")
    if not current_user:
        raise HTTPException(status_code=404, detail="Please check username")

    if not verify_password(user.password, str(current_user.password)):
        raise HTTPException(status_code=404, detail="wrong password")

    accessTokenExpiry = timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
    tokenExpiry = accessTokenExpiry + datetime.utcnow()
    tokenExpiryUnixTime = time.mktime(tokenExpiry.timetuple())
    accessToken = create_access_token(
        data={"email": user.email, "expiry": tokenExpiryUnixTime, "role": user.role},
        SECRET_KEY=SECRET_KEY,
        ALGORITHM=ALGORITHM,
        expires_delta=accessTokenExpiry,
    )

    return {
        "token": accessToken,
        "expiry": int(tokenExpiryUnixTime),
        "message": "success",
    }
