from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings

engine=create_async_engine(settings.DATABASE_URL,echo=True)
sessionlocal= async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):pass

async def get_db():
    async with sessionlocal() as session:
        yield session
    