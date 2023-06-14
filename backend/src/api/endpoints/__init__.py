from src.api.endpoints.auth import router as auth_router
from src.api.endpoints.account import router as user_router
from src.api.endpoints.products import router as products_router
from src.api.endpoints.cart import router as cart_router

routers_list = [auth_router, user_router, products_router, cart_router]
