from fastapi import HTTPException


from src.database.repository.cart_repo import CartRepository
from src.database.repository.products_repo import ProductRepository
from src.schemas.cart import CartSchema, UpdateCartSchema
from src.database import postgres


class ShoppingService:
    cart_repository: CartRepository
    product_repository: ProductRepository

    def __init__(self):
        self.cart_repository = CartRepository()
        self.product_repository = ProductRepository()

    async def get_cart(self, auth: dict):
        cart = await self.cart_repository.get_by_id(auth['id'])

        return cart

    async def add_product(self, auth: dict, product_id: str):
        await self.__check_product_id(product_id)

        amount = await self.__get_amount(auth['id'], product_id)

        try:
            if amount:
                result = await self.cart_repository.update(
                    auth['id'],
                    UpdateCartSchema(
                        product_id=product_id,
                        amount=amount + 1
                    )
                )
            else:
                result = await self.cart_repository.create(
                    CartSchema(
                        account_id=auth['id'],
                        product_id=product_id,
                        amount=1
                    )
                )
            await postgres.commit()
        except Exception:
            await postgres.rollback()
            raise HTTPException(
                status_code=400,
                detail='Cannot add product to cart'
            )

        return result

    async def remove_product(self, auth: dict, product_id: str):
        await self.__check_product_id(product_id)

        amount = await self.__get_amount(auth['id'], product_id)

        if amount == 0:
            raise HTTPException(
                status_code=404,
                detail='This product is not in your cart'
            )

        try:
            if amount == 1:
                result = await self.cart_repository.remove_product(auth['id'], product_id)
            else:
                result = await self.cart_repository.update(
                    auth['id'],
                    UpdateCartSchema(
                        product_id=product_id,
                        amount=amount - 1
                    )
                )
            await postgres.commit()
        except Exception as e:
            await postgres.rollback()
            raise HTTPException(
                status_code=400,
                detail='Cannot remove product from cart'
            )

        return result

    async def __check_product_id(self, product_id: str) -> None:
        product = await self.product_repository.get_by_id(product_id)

        if product is None:
            raise HTTPException(
                status_code=404,
                detail=f'Product with Id={product_id} is not exist'
            )

    async def __get_amount(self, account_id: int, product_id: str) -> int:
        product = await self.cart_repository.get_product_from_cart(account_id, product_id)

        return product

