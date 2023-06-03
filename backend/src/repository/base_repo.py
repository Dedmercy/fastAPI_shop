from typing import TypeVar, Generic, List
from pydantic import BaseModel

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete

from src.models.models import Base

Model = TypeVar("Model", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository:
    """
        Базовый класс, хранящий набор функций реализующий CRUD операции.

        :param model - Модель, той таблицы, с которой происходит взаимодействие
    """

    model = Generic[Model]

    @classmethod
    async def create(cls, schema: CreateSchemaType, session: AsyncSession) -> Model:
        schema_data = jsonable_encoder(schema)
        query = insert(cls.model).values(**schema_data).returning(cls.model)
        result = await session.execute(query)
        return result.scalars().one()

    @classmethod
    async def get_all(cls, session: AsyncSession) -> List[Model]:
        query = select(cls.model).order_by(cls.model.id)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_by_id(cls, id_: int, session: AsyncSession) -> Model:
        query = select(cls.model).where(cls.model.id == id_)
        result = await session.execute(query)
        return result.scalars().one_or_none()

    @classmethod
    async def update(cls, id_: int, schema: UpdateSchemaType, session: AsyncSession) -> Model:
        schema_data = jsonable_encoder(schema)
        query = update(cls.model).where(
            cls.model.id == id_
        ).values(**schema_data).returning(cls.model)
        result = await session.execute(query)
        return result.scalars().one()

    @classmethod
    async def delete(cls, id_: int, session: AsyncSession) -> Model:
        query = delete(cls.model).where(cls.model.id == id_).returning(cls.model)
        result = await session.execute(query)
        return result.scalars().one()
