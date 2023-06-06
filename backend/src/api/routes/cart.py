from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId

from src.repository.products_repo import ProductRepository
from src.auth.jwt import JWTRepository
from src.services import ShoppingService


router = APIRouter(
    prefix="/cart",
    tags=["cart"]
)


@router.put('/add/{product_id}/to_cart')
async def add_product_to_cart(product_id: str, auth: dict =  JWTRepository.verify_access_token):
    pass


@router.get('/my_cart')
async def get_my_cart(data: dict = Depends(JWTRepository.verify_access_token)):
    pass
