from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from datetime import datetime
from sqlalchemy import func
from sqlalchemy import ForeignKey


class Transaction(Base):
    __tablename__= 'transactions'

    transaction_id: Mapped[int]=mapped_column(primary_key=True)
    amount: Mapped[float]=mapped_column(nullable=False)
    merchant: Mapped[str]=mapped_column(nullable=False)
    category: Mapped[Optional[str]]= mapped_column()
    bank: Mapped[Optional[str]]=mapped_column()
    sms_text: Mapped[Optional[str]]=mapped_column()
    date: Mapped[datetime]= mapped_column()
    user_id: Mapped[int]= mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime]= mapped_column(server_default=func.now())
