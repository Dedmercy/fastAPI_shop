from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.base_repo import BasePostgresRepository, PostgresModel
from src.models.postgres_models import Account


class AccountRepository(BasePostgresRepository):
    model = Account

    @classmethod
    async def get_by_username(cls, username: str, session: AsyncSession) -> PostgresModel:
        query = select(cls.model).where(cls.model.username == username)
        result = await session.execute(query)
        return result.scalars().one_or_none()
