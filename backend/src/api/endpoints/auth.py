from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.jwt import JWTRepository
from src.auth.auth import AuthenticationHasher, oauth2_scheme
from src.schemas.auth import AccountSchema
from src.schemas.user import UserCreateSchema
from src.repository.account_repo import AccountRepository
from src.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authorisation"]
)


@router.post("/login")
async def authorisation(form_data: OAuth2PasswordRequestForm = Depends()):
    result = await AuthService().authentication(form_data)
    return result


@router.post("/registration")
async def registration(schema: UserCreateSchema):
    result = await AuthService().registration(schema)
    return result
