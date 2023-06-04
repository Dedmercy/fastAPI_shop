from src.repository.base_repo import BaseMongoRepository
from src.models.mongo_models import Product


class ProductRepository(BaseMongoRepository):
    model = Product
    ...

