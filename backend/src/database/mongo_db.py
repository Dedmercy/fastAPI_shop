from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from src.config import config
from src.models.mongo_models import Product


class MongoDB:
    """
        Класс для подключения к MongoDB.
    """
    db_url = f"mongodb://{config.mongo_username}:{config.mongo_password}@" \
             f"{config.mongo_host}:{config.mongo_port}"

    def __init__(self):
        self.client = None

    async def initialization(self):
        self.client = AsyncIOMotorClient(self.db_url)
        await init_beanie(self.client[config.mongo_database], document_models=[Product])


mongo = MongoDB()
