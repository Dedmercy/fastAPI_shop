from typing import TypeVar, Generic, List

from beanie.odm.operators.update.general import Set
from pydantic import BaseModel
from beanie import Document, PydanticObjectId

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete

from src.models.postgres_models import Base

PostgresModel = TypeVar("PostgresModel", bound=Base)
MongoModel = TypeVar("MongoModel", bound=Document)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BasePostgresRepository:
    """
        The base class that stores a set of functions that implements CRUD operations for PostgreSQL.
    """

    model = Generic[PostgresModel]

    @classmethod
    async def create(cls, schema: CreateSchemaType, session: AsyncSession) -> PostgresModel:
        """
            Inserting a new record in the database.
        """

        schema_data = jsonable_encoder(schema)
        query = insert(cls.model).values(**schema_data).returning(cls.model)
        result = await session.execute(query)
        return result.scalars().one()

    @classmethod
    async def get_all(cls, session: AsyncSession) -> List[PostgresModel]:
        """
            Getting all existing records in cls.model table.
        """

        query = select(cls.model).order_by(cls.model.id)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_by_id(cls, id_: int, session: AsyncSession) -> PostgresModel:
        """
            Getting record in cls.model table by id.
        """
        query = select(cls.model).where(cls.model.id == id_)
        result = await session.execute(query)
        return result.scalars().one_or_none()

    @classmethod
    async def update(cls, id_: int, schema: UpdateSchemaType, session: AsyncSession) -> PostgresModel:
        """
            Updating record in cls.model table.
        """
        schema_data = jsonable_encoder(schema)
        query = update(cls.model).where(
            cls.model.id == id_
        ).values(**schema_data).returning(cls.model)
        result = await session.execute(query)
        return result.scalars().one()

    @classmethod
    async def delete(cls, id_: int, session: AsyncSession) -> PostgresModel:
        """
            Deleting record in cls.model table.
        """
        query = delete(cls.model).where(cls.model.id == id_).returning(cls.model)
        result = await session.execute(query)
        return result.scalars().one()


class BaseMongoRepository:
    """
           The base class that stores a set of functions that implements CRUD operations for MongoDB.
    """
    model = Generic[MongoModel]

    @classmethod
    async def get_all(cls):
        """
            Getting all existing records in cls.model table.
        """
        result = await cls.model.find_all().to_list()
        return result

    @classmethod
    async def create(cls, schema: CreateSchemaType):
        """
            Inserting a new record in the database.
        """
        schema_data = jsonable_encoder(schema)
        new_document = cls.model(**schema_data)
        result = await cls.model.insert_one(new_document)
        return result

    @classmethod
    async def get_by_id(cls, id_: str):
        """
            Getting record in cls.model table by id.
        """
        result = await cls.model.find_one(cls.model.id == PydanticObjectId(id_))
        return result

    @classmethod
    async def update(cls, schema: UpdateSchemaType, id_: str):
        """
            Updating record in cls.model table.
        """
        schema_data = jsonable_encoder(schema)

        await cls.model.find_one(
            cls.model.id == PydanticObjectId(id_)
        ).update(Set(schema_data))

        result = await cls.model.find_one(cls.model.id == PydanticObjectId(id_))
        return result

    @classmethod
    async def delete(cls, id_: str):
        """
            Deleting record in cls.model table.
        """
        result = await cls.model.find_one(cls.model.id == PydanticObjectId(id_))

        await result.delete()
        return result
