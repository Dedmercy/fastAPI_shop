from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.config import config


class PostgresDB:
    """
        Класс для подключения к PostgreSQL
    """
    db_url = f"postgresql+asyncpg://{config.postgres_username}:{config.postgres_password}@" \
             f"{config.postgres_host}:{config.postgres_port}/{config.postgres_database}"

    def __init__(self):
        self.engine = None
        self.session = None

    async def initialization(self):
        self.engine = create_async_engine(self.db_url)
        self.session = async_sessionmaker(self.engine, expire_on_commit=False)()

    def __getattr__(self, item):
        return getattr(self.session, item)

postgres = PostgresDB()
