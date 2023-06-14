from typing import List

from fastapi import FastAPI, APIRouter

from src.database import mongo, postgres
from src.api.endpoints import routers_list


class AppCreator:
    """
        Class of initialization of an app.
    """
    __app: FastAPI

    def __init__(self):
        self.__app = FastAPI(
            title="Coffee shop",
            description="My coffee/tee shop"
        )
        self.register_events()
        self.register_routes()

    def get_app(self) -> FastAPI:
        """
            Getting the application instance.
        """
        return self.__app

    def register_events(self):
        @self.__app.on_event("startup")
        async def startup():
            await postgres.initialization()
            await mongo.initialization()

        @self.__app.on_event("shutdown")
        async def shutdown():
            await postgres.close()

    def register_routes(self):
        for router in routers_list:
            self.__app.include_router(router)
