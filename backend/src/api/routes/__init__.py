from src.api.routes.auth import router as auth_router
from src.api.routes.users import router as user_router
from src.api.routes.products import router as products_router
from src.api.routes.cart import router as cart_router

routers_list = [auth_router, user_router, products_router]
