from typing import List

from sqlalchemy import select, insert, update, delete

from src.database.repository.base_repo import BasePostgresRepository, PostgresModel, UpdateSchemaType
from src.database.models.postgres_models import Cart
from src.schemas.cart import CartSchema
from src.database import postgres


class CartRepository(BasePostgresRepository):
    model = Cart

    @classmethod
    async def get_by_id(cls, id_: int) -> List[PostgresModel]:
        query = select(cls.model).where(cls.model.account_id == int(id_))

        result = await postgres.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_product_from_cart(cls, account_id: int, product_id: str) -> int:
        query = select(cls.model).where(
            cls.model.account_id == account_id
            and
            cls.model.product_id == product_id
        )
        result = await postgres.execute(query)
        result = result.scalars().one_or_none()

        if result:
            return result.amount

        return 0

    @classmethod
    async def create(cls, schema: CartSchema) -> Cart:
        query = insert(cls.model).values(
            account_id=int(schema.account_id),
            product_id=schema.product_id
        ).returning(cls.model)

        result = await postgres.execute(query)

        return result.scalars().one()

    @classmethod
    async def update(cls, id_: int, schema: UpdateSchemaType) -> PostgresModel:
        query = update(cls.model).where(
            cls.model.account_id == id_
            and
            cls.model.product_id == schema.product_id
        ).values(
            amount=schema.amount
        ).returning(cls.model)

        result = await postgres.execute(query)

        return result.scalars().one()

    @classmethod
    async def remove_product(cls, account_id: int, product_id: str) -> PostgresModel:
        query = delete(cls.model).where(
            cls.model.account_id == account_id
            and
            cls.model.product_id == product_id
        ).returning(cls.model)

        result = await postgres.execute(query)
        result = result.scalars().one()

        return result
