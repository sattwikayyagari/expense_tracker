from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class SMSMessage(BaseModel):
    raw_sms: str

class TransactionCreate(BaseModel):
    amount: float
    merchant: str
    bank: Optional[str]
    date: datetime

class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    merchant: Optional[str] = None
    bank: Optional[str] = None
    date: Optional[datetime] = None

class TransactionRead(BaseModel):
    id: int
    amount: float
    merchant: str
    bank: Optional[str]
    category: Optional[str]
    date: datetime
    created_at: datetime

    model_config=ConfigDict(from_attributes=True)