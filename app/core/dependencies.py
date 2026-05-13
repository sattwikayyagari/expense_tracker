from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.core.security import verify_token
from app.crud.user import get_user_by_id

oauth2_scheme= OAuth2PasswordBearer(tokenUrl="/users/login")

async def get_current_user(token: str= Depends(oauth2_scheme), db: AsyncSession= Depends(get_db)):
    jwt_token_payload=verify_token(token)
    if not jwt_token_payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Password")
    payload_user_id=jwt_token_payload["user_id"]
    db_user= await get_user_by_id(db, payload_user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


