from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.base_repo import BasePostgresRepository, PostgresModel
from src.models.postgres_models import Account
from src.database import postgres


class AccountRepository(BasePostgresRepository):

    model = Account

    @classmethod
    async def get_by_username(cls, username: str) -> PostgresModel:
        query = select(cls.model).where(cls.model.username == username)
        result = await postgres.execute(query)
        return result.scalars().one_or_none()
