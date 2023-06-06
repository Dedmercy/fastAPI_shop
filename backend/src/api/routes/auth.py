from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.jwt import JWTRepository
from src.auth.auth import AuthenticationHasher, oauth2_scheme
from src.schemas.auth import AuthBase, AccountBase
from src.repository.account_repo import AccountRepository
from src.database.postgres_db import postgres_db

router = APIRouter(
    prefix="/auth",
    tags=["Authorisation"]
)


@router.post("/login")
async def authorisation(form_data: OAuth2PasswordRequestForm = Depends()):
    async with postgres_db.session() as session:
        account = await AccountRepository.get_by_username(form_data.username, session)

    if not account:
        raise HTTPException(
            status_code=403,
            detail=f"User with username:{form_data.username} is not exists"
        )

    hashed_password = AuthenticationHasher.get_hashed_password(form_data.password)

    if AuthenticationHasher.verify_password(form_data.password, account.password):
        token = JWTRepository.create_access_token(
            AccountBase(
                username=form_data.username,
                password=hashed_password,
                role_id=account.role_id
            )
        )
        return {
            "access_token": token,
            "token_Type": "bearer"
        }

    raise HTTPException(
        status_code=403,
        detail="Wrong password"
    )


@router.get('/my_account')
async def get_my_account(data: dict = Depends(JWTRepository.check_admin)):
    return data

