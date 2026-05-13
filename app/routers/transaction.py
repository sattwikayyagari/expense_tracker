from fastapi import Depends, APIRouter, HTTPException, status
from app.schemas.transaction import TransactionCreate, TransactionRead, TransactionUpdate, SMSMessage
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.crud.transaction import (create_transaction as crud_create_transaction, get_all_transactions as crud_get_all_transactions, get_transaction as crud_get_transaction, update_transaction as crud_update_transaction, delete_transaction as crud_delete_transaction, get_transaction_by_date as crud_get_transaction_by_date,
get_transaction_by_category as crud_get_transaction_by_category, get_transaction_by_date_category)
from typing import List
from datetime import datetime
from app.services.sms_parser import parse_sms



router=APIRouter(prefix="/transactions",tags=["transactions"])

@router.post("/create",response_model=TransactionRead, status_code=201)
async def create_transaction(transaction: TransactionCreate , db: AsyncSession=Depends(get_db), user: User= Depends(get_current_user)):
    new_transaction= await crud_create_transaction(db, transaction, user.id)
    return new_transaction

@router.post("/sms",response_model=TransactionRead, status_code=200)
async def submit_sms(sms_message: SMSMessage,db: AsyncSession=Depends(get_db), user: User=Depends(get_current_user)):
    parsed_sms= parse_sms(sms_message.raw_sms)
    if not parsed_sms:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="SMS could not be parsed")
    try:
        date=datetime.strptime(parsed_sms["date"],"%d-%b-%y")
    except ValueError:
        try:
            date=datetime.strptime(parsed_sms["date"],"%Y-%m-%d")
        except:
            date=datetime.strptime(parsed_sms["date"],"%d%b%y")
    parsed_transaction=TransactionCreate(
        amount=parsed_sms["amount"],
        merchant=parsed_sms["merchant"],
        bank=parsed_sms["bank"],
        date=date
    )
    created_transaction= await crud_create_transaction(db, parsed_transaction, user.id)
    return created_transaction

@router.get("/",  response_model=List[TransactionRead], status_code=200)
async def get_all_transactions(db: AsyncSession = Depends(get_db), user: User= Depends(get_current_user)):
    db_transaction= await crud_get_all_transactions(db,user.id )
    return db_transaction

@router.get("/{transaction_id}",response_model=TransactionRead, status_code=200)
async def get_transaction(transaction_id: int, db: AsyncSession= Depends(get_db), user: User= Depends(get_current_user)):
    returned_transaction= await crud_get_transaction(db, transaction_id)
    if not returned_transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction Not Found")
    if returned_transaction.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong User")
    return returned_transaction

@router.patch("/{transaction_id}",response_model=TransactionRead, status_code=200)
async def update_transaction(transaction_id: int, transaction: TransactionUpdate, db: AsyncSession= Depends(get_db), user: User= Depends(get_current_user)):
    db_transaction= await crud_get_transaction(db, transaction_id)
    if not db_transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction Not found")
    if db_transaction.user_id!= user.id:
        raise HTTPException (status_code=status.HTTP_403_FORBIDDEN, detail="Wrong User") 
    updated_crud= await crud_update_transaction(db, transaction_id, transaction)
    return updated_crud

@router.delete("/{transaction_id}", status_code=200)
async def delete_user(transaction_id: int, db: AsyncSession = Depends(get_db), user: User =Depends(get_current_user)):
    db_transaction= await crud_get_transaction(db, transaction_id)
    if not db_transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    if db_transaction.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong User")
    await crud_delete_transaction(db, transaction_id)
    return f"Transaction with id {transaction_id} successfully removed"

@router.get("/filter/date",response_model=List[TransactionRead], status_code=200)
async def get_transaction_by_date(start_date: datetime, end_date: datetime, db: AsyncSession=Depends(get_db), user:User= Depends(get_current_user)):
    db_transaction= await crud_get_transaction_by_date(db, user.id, start_date, end_date)
    return db_transaction

@router.get("/filter/category",response_model=List[TransactionRead], status_code=200)
async def get_transaction_by_category(category: str, db: AsyncSession=Depends(get_db), user: User= Depends(get_current_user)):
    db_transaction= await crud_get_transaction_by_category(db, user.id, category)
    return db_transaction

@router.get("/filter/date_and_category",response_model=List[TransactionRead], status_code=200)
async def get_transaction_by_date_and_category(category: str, start_date: datetime, end_date: datetime, db: AsyncSession= Depends(get_db), user: User=Depends(get_current_user)):
    db_transaction= await get_transaction_by_date_category(db, user.id, start_date, end_date, category)
    return db_transaction