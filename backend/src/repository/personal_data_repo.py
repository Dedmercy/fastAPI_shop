from src.repository.base_repo import BasePostgresRepository
from src.models.postgres_models import Account, PersonalData


class PersonalDataRepository(BasePostgresRepository):
    model = PersonalData
