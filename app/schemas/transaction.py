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

class TransactionRead(BaseModel):
    id: int
    amount: float
    merchant: str
    bank: Optional[str]
    category: Optional[str]
    date: datetime
    created_at: datetime

    model_config=ConfigDict(from_attributes=True)