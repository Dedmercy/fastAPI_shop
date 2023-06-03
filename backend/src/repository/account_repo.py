from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.base_repo import BaseRepository, Model
from src.models.models import Account, PersonalData


class AccountRepository(BaseRepository):
    model = Account

    @classmethod
    async def get_by_username(cls, username: str, session: AsyncSession) -> Model:
        query = select(cls.model).where(cls.model.username == username)
        result = await session.execute(query)
        return result.scalars().one_or_none()
