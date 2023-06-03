from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

from src.schemas.user import UserCreateBase, AccountCreateBase, PersonalDataCreateBase
from src.schemas.user import UserUpdateBase, PersonalDataUpdateBase, AccountUpdateBase
from src.repository.account_repo import AccountRepository
from src.repository.personal_data_repo import PersonalDataRepository
from src.database.postgres_db import postgres_db

router = APIRouter(
    prefix='/users',
    tags=["Users"]
)


@router.get('/all')
async def get_all_accounts():
    async with postgres_db.session() as session:

        accounts = await AccountRepository.get_all(session)

    if len(accounts) == 0:
        raise HTTPException(
            status_code=404, detail="We dont have users :("
        )

    account_data = [account.as_dict() for account in accounts]

    return {"data": account_data}


@router.get('/by_id')
async def get_account_by_id(id_: int):
    async with postgres_db.session() as session:

        account = await AccountRepository.get_by_id(id_, session)

        if not account:
            raise HTTPException(
                status_code=404, detail=f"Account with id={id_} not found"
            )

    account = account.as_dict()

    return {"data": account}


@router.post('/create')
async def create_account(obj_in: UserCreateBase):

    async with postgres_db.session() as session:
        account_by_username = await AccountRepository.get_by_username(obj_in.username, session)

    if account_by_username:
        raise HTTPException(
            status_code=404, detail=f"Account with username={obj_in.username} already exists"
        )

    if obj_in.role_id not in (1, 2):
        raise HTTPException(
            status_code=404, detail=f"Role with id={obj_in.role_id} not exists"
        )

    account = AccountCreateBase(
        username=obj_in.username,
        password=obj_in.password,
        role_id=obj_in.role_id
    )

    personal_data = PersonalDataCreateBase(
        id=0,
        first_name=obj_in.first_name,
        middle_name=obj_in.middle_name,
        last_name=obj_in.last_name,
        email=obj_in.email,
        phone=obj_in.phone
    )

    async with postgres_db.session() as session:
        try:
            account = await AccountRepository.create(account, session)
            personal_data.id = account.id
            personal_data = await PersonalDataRepository.create(personal_data, session)
            await session.commit()
        except Exception as e:
            # TODO СДелать логи
            # TODO Сделать отлов ошибок
            print(e)
            await session.rollback()
            return {"message": "error"}

    return {"inserted_date": {"inserted_account": account.as_dict(), "inserted_personal_data": personal_data.as_dict()}}


@router.put('/update')
async def update_account(id_: int, obj_in: UserUpdateBase):

    account_update = AccountUpdateBase(
        username=obj_in.username,
        password=obj_in.password
    )

    personal_data_update = PersonalDataUpdateBase(
        first_name=obj_in.first_name,
        middle_name=obj_in.middle_name,
        last_name=obj_in.last_name,
        email=obj_in.email,
        phone=obj_in.phone
    )

    # Проверим, существует ли запись с необходимым id
    async with postgres_db.session() as session:
        account_by_id = await AccountRepository.get_by_id(id_, session)
        account_by_username = await AccountRepository.get_by_username(obj_in.username, session)

    if not account_by_id:
        raise HTTPException(
            status_code=404, detail=f"Account with id={id_} not found"
        )

    if account_by_username:
        raise HTTPException(
            status_code=404, detail=f"Account with username={obj_in.username} already exists"
        )

    async with postgres_db.session() as session:
        try:
            account = await AccountRepository.update(id_, account_update, session)
            personal_data = await PersonalDataRepository.update(id_, personal_data_update, session)
            await session.commit()
        except Exception as e:
            print(e)
            await session.rollback()
            return {"message": "error"}

    return {"updated_data": {"updated_account": account.as_dict(), "updated_personal_data": personal_data.as_dict()}}


@router.delete('/delete')
async def delete_account(id_: int):
    async with postgres_db.session() as session:

        account = await AccountRepository.get_by_id(id_, session)

    if not account:
        raise HTTPException(
            status_code=404, detail=f"Account with id={id_} not found"
        )

    async with postgres_db.session() as session:
        try:
            deleted_personal_data = await PersonalDataRepository.delete(id_, session)
            deleted_account = await AccountRepository.delete(id_, session)
            await session.commit()
        except Exception as e:
            print(e)
            await session.rollback()
            return {"message": "error"}

        return {
            "deleted_data": {
                "deleted_account": deleted_account.as_dict(),
                "deleted_personal_data": deleted_personal_data.as_dict()
            }
        }
