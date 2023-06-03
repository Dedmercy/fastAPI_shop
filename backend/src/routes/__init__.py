from src.routes.auth import router as auth_router
from src.routes.users import router as user_router
from src.routes.products import router as products_router

routers_list = [auth_router, user_router, products_router]
