from app.schemas.transaction import TransactionCreate, TransactionUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.transaction import Transaction
from sqlalchemy import select
from datetime import datetime

async def create_transaction(db: AsyncSession, transaction: TransactionCreate, user_id: int):
    db_transaction= Transaction(
        amount=transaction.amount,
        merchant=transaction.merchant,
        bank=transaction.bank,
        date=transaction.date,
        user_id=user_id
    )
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction

async def get_transaction(db:AsyncSession,transaction_id: int):
    result= await db.execute(select(Transaction).where(Transaction.transaction_id==transaction_id))
    return result.scalar_one_or_none()

async def get_all_transactions(db:AsyncSession, user_id: int):
    result=await db.execute(select(Transaction).where(Transaction.user_id==user_id))
    return result.scalars().all()

async def get_transaction_by_date(db:AsyncSession,user_id: int,start_date: datetime, end_date: datetime):
    result=await db.execute(select(Transaction).where(Transaction.user_id==user_id,Transaction.date>=start_date, Transaction.date<=end_date))
    return result.scalars().all()

async def get_transaction_by_category(db: AsyncSession, user_id: int, category: str):
    result=await db.execute(select(Transaction).where(Transaction.user_id==user_id, Transaction.category==category))
    return result.scalars().all()

async def get_transaction_by_date_category(db: AsyncSession, user_id: int, start_date: datetime, end_date: datetime, category: str):
    result=await db.execute(select(Transaction).where(Transaction.user_id==user_id, Transaction.date>=start_date, Transaction.date<=end_date, Transaction.category==category))
    return result.scalars().all()

async def update_transaction(db: AsyncSession, transaction_id: int, transaction: TransactionUpdate):
    db_transaction= await get_transaction(db, transaction_id)

    if transaction.amount is not None:
        db_transaction.amount=transaction.amount
    if transaction.merchant is not None:
        db_transaction.merchant=transaction.merchant
    if transaction.bank is not None:
        db_transaction.bank=transaction.bank
    if transaction.date is not None:
        db_transaction.date=transaction.date

    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction

async def delete_transaction(db: AsyncSession, transaction_id: int):
    db_transaction= await get_transaction(db, transaction_id)

    await db.delete(db_transaction)
    await db.commit()
    return f"Transaction with id {transaction_id} successfully deleted"