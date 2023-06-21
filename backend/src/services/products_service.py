from bson import ObjectId
from fastapi import HTTPException, status

from src.database.repository.products_repo import ProductRepository
from src.schemas.product import CreateProductSchema, UpdateProductSchema


class ProductService:
    def __init__(self):
        self.__product_repo = ProductRepository()

    async def create_product(self, schema: CreateProductSchema):
        result = await self.__product_repo.create(schema)

        return result

    async def update_product(self, product_id: str, schema: UpdateProductSchema):
        result = await self.__product_repo.update(schema, product_id)

        return result

    async def delete_product(self, product_id: str):
        result = await self.__product_repo.delete(product_id)

        return result

    async def get_products_by_price(self, start: int, end: int):
        result = await self.__product_repo.get_products_by_price(start, end)

        return result

    async def get_products_by_category(self, category: str):
        result = await self.__product_repo.get_products_by_category(category)
        return result

    async def get_all_products(self):
        result = await self.__product_repo.get_all()

        return result

    async def get_product_by_id(self, product_id: str):
        product_id_is_valid(product_id)

        result = await self.__product_repo.get_by_id(product_id)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID:{product_id} is not exist"
            )

        return result


def product_id_is_valid(product_id: str):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"ID:{product_id} is not valid ObjectId, it must be a 12-byte input or a 24-character hex string"
        )
