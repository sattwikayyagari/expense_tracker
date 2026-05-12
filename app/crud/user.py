from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from sqlalchemy import select
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_hashed_password

async def get_user_by_email(db:AsyncSession, email: str):
    db_user= await db.execute(select(User).where(User.email==email))
    return db_user.scalar_one_or_none()

async def get_user_by_id(db: AsyncSession, id: int):
    db_user= await db.execute(select(User).where(User.id==id))
    return db_user.scalar_one_or_none()

async def create_user(db: AsyncSession, user: UserCreate):
    existing_user= await get_user_by_email(db, user.email)

    if existing_user:
        raise ValueError("User already exists")
    db_user= User(
        email= user.email,
        hashed_password=get_hashed_password(user.password)
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user(db:AsyncSession, user: UserUpdate, user_id: int):
    db_user=await get_user_by_id(db, user_id)

    if user.email is not None:
        db_user.email=user.email
    if user.password is not None:
        db_user.hashed_password=get_hashed_password(user.password)
    
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def delete_user(db: AsyncSession, user_id: int):
    db_user=await get_user_by_id(db, user_id)
    await db.delete(db_user)
    await db.commit()
    return f"User with id {user_id} successfully deleted"