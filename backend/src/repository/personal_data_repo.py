from sqlalchemy import select

from src.repository.base_repo import BaseRepository
from src.models.models import Account, PersonalData

from src.database.postgres_db import postgres_db


class PersonalDataRepository(BaseRepository):
    model = PersonalData

