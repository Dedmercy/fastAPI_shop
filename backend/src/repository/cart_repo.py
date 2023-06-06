from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.repository.base_repo import BasePostgresRepository, PostgresModel
from src.models.postgres_models import Cart


class CartRepository(BasePostgresRepository):
    model = Cart

    @classmethod
    async def get_by_id(cls, id_: int, session: AsyncSession) -> List[PostgresModel]:
        query = select(cls.model).where(cls.model.account_id == id_)

        result = await session.execute(query)
        return result.scalars().all()


