from fastapi import APIRouter, status

from src.services.products_service import ProductService

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/all")
async def get_all_products():
    result = await ProductService().get_all_products()

    return {
        "status": "OK",
        "data": [*result],
    }


@router.get("/by-category")
async def get_products_by_category(category: str):
    result = await ProductService().get_products_by_category(category)

    return {
        "status": "OK",
        "data": [*result]
    }


@router.get("/by-price/between/")
async def get_products_by_price(start: int, end: int):
    result = await ProductService().get_products_by_price(start, end)

    return {
        "status": "OK",
        "data": [*result]
    }
