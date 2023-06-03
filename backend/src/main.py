import uvicorn

from fastapi import FastAPI
from src.database.postgres_db import postgres_db
from src.routes import routers_list
from src.server import App


def create_app() -> FastAPI:
    app = FastAPI(
            title="Coffee shop",
            description="My coffee shop"
    )

    return App(app).get_app()


app = create_app()


@app.on_event("startup")
async def startup():
    postgres_db.initialization()


@app.on_event("shutdown")
async def shutdown():
    pass


if __name__ == '__main__':
    uvicorn.run(app='main:app', host='127.0.0.1', port=8080, reload=True)
