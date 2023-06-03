from fastapi import FastAPI
from database.postgres_db import postgres_db
from routes import routers_list


class App:
    """
        Класс для инициализации приложения
    """
    __app: FastAPI

    def __init__(self, app: FastAPI):
        self.__app = app
        # self.register_events(self.__app)
        self.register_routes(self.__app)

    def get_app(self) -> FastAPI:
        return self.__app

    @staticmethod
    def register_events(app: FastAPI):
        app.on_event("startup")(postgres_db.initialization)

    @staticmethod
    def register_routes(app: FastAPI):
        for router in routers_list:
            app.include_router(router)
