from sqlalchemy import select

from src.repository.base_repo import BasePostgresRepository
from src.models.postgres_models import Account, PersonalData
from src.database import postgres


class PersonalDataRepository(BasePostgresRepository):
    model = PersonalData

    @classmethod
    async def get_by_email(cls, email: str):
        query = select(cls.model).where(cls.model.email == email)
        result = await postgres.execute(query)

        return result.scalars().one_or_none()
