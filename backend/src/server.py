from fastapi import FastAPI
from database.postgres_db import postgres_db
from src.api.routes import routers_list


class App:
    """
        Class of initialization of an app.
    """
    __app: FastAPI

    def __init__(self, app: FastAPI):
        self.__app = app
        # self.register_events(self.__app)
        self.register_routes(self.__app)

    def get_app(self) -> FastAPI:
        """
            Getting the application instance.
        """
        return self.__app

    @staticmethod
    def register_events(app: FastAPI):
        pass

    @staticmethod
    def register_routes(app: FastAPI):
        """
            Set routes to the app instance.
        """
        for router in routers_list:
            app.include_router(router)
