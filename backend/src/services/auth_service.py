from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.auth import AuthenticationHasher
from src.auth.jwt import JWTRepository
from src.database import postgres
from src.repository.account_repo import AccountRepository
from src.schemas.auth import AccountSchema
from src.repository.personal_data_repo import PersonalDataRepository
from src.schemas.user import UserCreateSchema, AccountCreateSchema, PersonalDataCreateSchema


class AuthService:
    account_repository: AccountRepository
    personal_data_repository: PersonalDataRepository
    hasher: AuthenticationHasher
    jwt_repository: JWTRepository

    def __init__(self):
        self.account_repository = AccountRepository()
        self.personal_data_repository = PersonalDataRepository()
        self.hasher = AuthenticationHasher()
        self.jwt_repository = JWTRepository()

    async def authentication(self, schema: OAuth2PasswordRequestForm):
        account = await self.account_repository.get_by_username(schema.username)

        if not account:
            raise HTTPException(
                status_code=403,
                detail=f"User with username:{schema.username} is not exists"
            )

        hashed_password = self.hasher.get_hashed_password(schema.password)

        if self.hasher.verify_password(schema.password, account.password):
            data = AccountSchema(
                id=account.id,
                username=schema.username,
                password=hashed_password,
                role_id=account.role_id
            )

            token = self.jwt_repository.create_access_token(data)

            return {
                "access_token": token,
                "token_Type": "bearer"
            }

        raise HTTPException(
            status_code=403,
            detail="Wrong password"
        )

    async def registration(self, schema: UserCreateSchema):
        """
            Registration a new user.
        """
        await self.__validate_new_user(schema)

        account = self.__create_account_schema(schema)
        personal_data = self.__create_personal_data_schema(schema)

        try:
            account = await self.account_repository.create(account)
            personal_data.id = account.id
            personal_data = await self.personal_data_repository.create(personal_data)
            await postgres.commit()
        except Exception as e:
            # TODO СДелать логи
            # TODO Сделать отлов ошибок
            await postgres.rollback()
            return {"message": "error"}

        return {
            "inserted_date": {
                "inserted_account": account.as_dict(),
                "inserted_personal_data": personal_data.as_dict()
            }
        }

    async def __validate_new_user(self, schema: UserCreateSchema) -> None:
        """
            Input data validation.
        """
        await self.__validate_uniqueness_username(schema.username)
        await self.__validate_uniqueness_email(schema.email)

    async def __validate_uniqueness_username(self, username: str) -> None:
        """
            Uniqueness check for user-entered username.
        """
        data_by_username = await self.account_repository.get_by_username(username)

        if data_by_username:
            raise HTTPException(
                status_code=404, detail=f"Account with username={username} already exists"
            )

    async def __validate_uniqueness_email(self, email: str) -> None:
        """
            Uniqueness check for user-entered username.
        """
        data_by_email = await self.personal_data_repository.get_by_email(email)

        if data_by_email:
            raise HTTPException(
                status_code=404, detail=f"Account with email={email} already exists"
            )

    def __create_account_schema(self, all_data: UserCreateSchema) -> AccountCreateSchema:
        """
            Create Account schema for inserting data in database.
        """
        return AccountCreateSchema(
            username=all_data.username,
            password=self.hasher.get_hashed_password(all_data.password),
            role_id=1
        )

    @staticmethod
    def __create_personal_data_schema(all_data: UserCreateSchema) -> PersonalDataCreateSchema:
        """
           Create Personal Data schema for inserting data in database.
        """
        return PersonalDataCreateSchema(
            id=0,
            first_name=all_data.first_name,
            middle_name=all_data.middle_name,
            last_name=all_data.last_name,
            email=all_data.email,
            phone=all_data.phone
        )
