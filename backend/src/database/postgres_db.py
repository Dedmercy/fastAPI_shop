from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import sessionmaker

from src.config import config

DB_URL = f"postgresql+asyncpg://{config.postgres_username}:{config.postgres_password}@" \
         f"{config.postgres_host}:{config.postgres_port}/{config.postgres_database}"


class AsyncPostgresSession:

    def __init__(self):
        self.session = None
        self.engine = None

    def __getattr__(self, item):
        getattr(self.session, item)

    def initialization(self):
        self.engine = create_async_engine(DB_URL)
        self.session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)


postgres_db = AsyncPostgresSession()
