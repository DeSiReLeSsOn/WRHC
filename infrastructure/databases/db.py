from sqlalchemy.ext.asyncio import (create_async_engine, 
                                    AsyncSession, 
                                    async_sessionmaker)
from .config import PostgresConfig
from .models import Base


config = PostgresConfig()


engine = create_async_engine(
    f"postgresql+asyncpg://{config.user}:{config.password}@{config.host}:{config.port}/{config.database}",
    pool_pre_ping=True,
    echo=True,
)

AsyncSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


async def get_db_async():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    await engine.dispose()