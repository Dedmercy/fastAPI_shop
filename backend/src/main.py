import uvicorn

from fastapi import FastAPI
from src.database.postgres_db import postgres_db
from src.database.mongo_db import mongo_db
from src.server import App


def create_app() -> FastAPI:
    app = FastAPI(
            title="Coffee shop",
            description="My coffee/tee shop"
    )

    return App(app).get_app()


app = create_app()


@app.on_event("startup")
async def startup():
    await postgres_db.initialization()
    await mongo_db.initialization()


@app.on_event("shutdown")
async def shutdown():
    pass


if __name__ == '__main__':
    uvicorn.run(app='main:app', host='127.0.0.1', port=8080, reload=True)
