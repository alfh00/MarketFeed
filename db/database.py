import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.future import select


Base = declarative_base()

# Create an async engine
host=os.getenv("DB_HOST")
database=os.getenv("DB_NAME")
user=os.getenv("DB_USER")
password=os.getenv("DB_PASS")

DATABASE_URL = f"postgresql://{user}:{password}@{host}/{database}"
engine = create_async_engine(DATABASE_URL, echo=True)

# Use async sessionmaker
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Entity(Base):
    __abstract__ = True

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs):
        obj = cls(**kwargs)
        session.add(obj)
        await session.commit()
        return obj

    @classmethod
    async def read(cls, session: AsyncSession, **kwargs):
        if not kwargs:
            return None

        query = select(cls)
        for attribute, value in kwargs.items():
            if hasattr(cls, attribute):
                filter_expr = getattr(cls, attribute) == value
                query = query.filter(filter_expr)
            else:
                raise AttributeError(f"{cls.__name__} has no attribute '{attribute}'")

        result = await session.execute(query)
        return result.scalars().first()

    async def update(self, session: AsyncSession, **kwargs):
        for key, value in kwargs.items():
            if key != 'id':  # Exclude updating the primary key
                setattr(self, key, value)
        await session.commit()
        return self

    @classmethod
    async def filter_by_keyword(cls, session: AsyncSession, **kwargs):
        query = select(cls)
        for attribute, value in kwargs.items():
            if hasattr(cls, attribute):
                filter_expr = getattr(cls, attribute) == value
                query = query.filter(filter_expr)
            else:
                raise AttributeError(f"{cls.__name__} has no attribute '{attribute}'")

        result = await session.execute(query)
        return result.scalars().all()

    async def delete(self, session: AsyncSession):
        await session.delete(self)
        await session.commit()
        return True

    @classmethod
    async def list_all(cls, session: AsyncSession):
        result = await session.execute(select(cls))
        return result.scalars().all()
