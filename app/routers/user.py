from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.crud.user import create_user, get_user_by_email, get_user_by_id, update_user as crud_update_user, delete_user as crud_delete_user

router=APIRouter(prefix='/users', tags=["users"])

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(user: UserCreate, db: AsyncSession= Depends(get_db)):
    db_user=await get_user_by_email(db,user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    new_user=await create_user(db, user)
    return  new_user

@router.get("/{user_id}",response_model=UserResponse, status_code=200)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user= await get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@router.patch("/{user_id}", response_model=UserResponse, status_code=200)
async def update_user(user_id: int, user: UserUpdate, db: AsyncSession= Depends(get_db)):
    db_user= await get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    updated_user= await crud_update_user(db, user, user_id)
    return updated_user

@router.delete("/{user_id}", status_code=200)
async def delete_user(user_id: int, db: AsyncSession=Depends(get_db)):
    db_user= await get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    await crud_delete_user(db, user_id)
    return f"User with id {user_id} successfully deleted"