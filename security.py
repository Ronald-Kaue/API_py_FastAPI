from pwdlib import PasswordHash
from http import HTTPStatus
from jwt import decode, encode
from jwt.exceptions import PyJWTError
from models.usuario import Usuario
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from database import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
import os 
from dotenv import load_dotenv

load_dotenv()
pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})

    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def current_user(session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email= payload.get('sub')
        if not email:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    
    user = session.scalar(select(Usuario).where(Usuario.email == email))

    if not user:
        raise credentials_exception
    
    return user