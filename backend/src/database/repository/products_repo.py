from beanie.operators import GTE, LTE, And

from src.database.repository.base_repo import BaseMongoRepository
from src.database.models.mongo_models import Product


class ProductRepository(BaseMongoRepository):
    model = Product

    @classmethod
    async def get_products_by_category(cls, category: str):
        result = await cls.model.find(cls.model.category == category).to_list()

        return result

    @classmethod
    async def get_products_by_price(cls, start: int, end: int):
        result = await cls.model.find(And(
                GTE(cls.model.price, start),
                LTE(cls.model.price, end)
            )
        ).to_list()
        return result


