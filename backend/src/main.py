import uvicorn


from src.server import AppCreator

application = AppCreator()
app = application.get_app()


if __name__ == '__main__':
    uvicorn.run(app='main:app', host='127.0.0.1', port=8080, reload=True)
