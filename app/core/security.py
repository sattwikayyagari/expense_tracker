from passlib.context import CryptContext
from jose import jwt, JWTError
from app.core.config import settings
from datetime import datetime, timedelta, timezone


pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def get_hashed_password(password: str):
    hashed_pwd=pwd_context.hash(password)
    return hashed_pwd

def verify_hashed_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)

def create_access_token(user_id: int):
    payload= {'user_id': user_id, 'exp': datetime.now(timezone.utc)+timedelta(hours=24)}
    token=jwt.encode(payload, key=settings.SECRET_KEY, algorithm="HS256")
    return token

def verify_token(token: str):
    try:
        payload=jwt.decode(token, key=settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        return None