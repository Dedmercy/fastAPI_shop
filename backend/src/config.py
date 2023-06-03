import os

from typing import Dict
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseModel):
    """
        Класс, содержащий данные о конфиге
    """

    # Postgres
    postgres_username: str
    postgres_password: str
    postgres_database: str
    postgres_host: str
    postgres_port: str

    # Mongo
    mongo_username: str
    postgres_password: str
    mongo_database: str
    mongo_host: str
    mongo_port: str

    class Config:
        frozen = True


def get_config():
    __config_params: Dict[str, str]
    __config_params = {param: os.environ.get(param.upper()) for param in Settings.__fields__}

    return Settings(**__config_params)


config = get_config()
