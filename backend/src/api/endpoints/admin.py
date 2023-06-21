from fastapi import APIRouter, Depends, status

from src.auth.jwt import JWTRepository
from src.database.repository.products_repo import ProductRepository
from src.schemas.product import CreateProductSchema, UpdateProductSchema

router = APIRouter(
    prefix="/admin",
    tags=["Admin functions"]
)


@router.post("/add-product", status_code=status.HTTP_201_CREATED)
async def add_product(obj_in: CreateProductSchema, auth: dict = Depends(JWTRepository.check_admin)):
    result = await ProductRepository().create(obj_in)

    return {
        "status": "OK",
        "data": result
    }


@router.put("/update-product", status_code=status.HTTP_200_OK)
async def update_product(
        product_id: str,
        obj_in: UpdateProductSchema,
        auth: dict = Depends(JWTRepository.check_admin)
):
    result = await ProductRepository().update(obj_in, product_id)

    return {
        "status": "OK",
        "data": result
    }


@router.delete("/delete-product", status_code=status.HTTP_200_OK)
async def delete_product(
        product_id: str,
        auth: dict = Depends(JWTRepository.check_admin)

):
    result = await ProductRepository.delete(product_id)
    return {
        "status": "OK",
        "data": result
    }
