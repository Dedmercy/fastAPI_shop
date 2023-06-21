from fastapi import APIRouter, Depends

from src.auth.jwt import JWTRepository
from src.services import ShoppingService

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


@router.get('/my_cart')
async def get_my_cart(auth: dict = Depends(JWTRepository.verify_access_token)):
    result = await ShoppingService().get_cart(auth)
    return result


@router.put('/add')
async def add_product_to_cart(product_id: str, auth: dict = Depends(JWTRepository.verify_access_token)):
    result = await ShoppingService().add_product(auth, product_id)
    return result


@router.put('/remove/{product_id}')
async def remove_product_from_cart(product_id: str, auth: dict = Depends(JWTRepository.verify_access_token)):
    result = await ShoppingService().remove_product(auth, product_id)
    return result
