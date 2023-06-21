from src.database.repository.account_repo import AccountRepository
from src.database.repository.personal_data_repo import PersonalDataRepository


class AccountService:
    account_repository: AccountRepository
    personal_data_repository: PersonalDataRepository

    def __init__(self):
        self.account_repository = AccountRepository()
        self.personal_data_repository = PersonalDataRepository()

    async def get_my_account(self, auth_data: dict):
        account = await self.account_repository.get_by_username(auth_data['username'])
        personal_data = await self.personal_data_repository.get_by_id(account.id)

        return {
            'data':
                {
                    'account': account,
                    'personal_data': personal_data
                }
        }

    async def update_account_data(self, auth_data: dict):
        pass

    async def update_password(self):
        pass
