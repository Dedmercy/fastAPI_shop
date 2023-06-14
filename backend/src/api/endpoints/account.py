from fastapi import APIRouter, Depends

from src.services.account_service import AccountService
from src.services.shopping_service import ShoppingService
from src.auth.jwt import JWTRepository

router = APIRouter(
    prefix='/me',
    tags=["Account Info"]
)


@router.get('/account')
async def get_my_account(auth: dict = Depends(JWTRepository.verify_access_token)):
    result = await AccountService().get_my_account(auth)
    return result


