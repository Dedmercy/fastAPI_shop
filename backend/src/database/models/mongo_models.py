from typing import Optional


from beanie import Document


class Product(Document):
    name: str
    description: Optional[str]
    category: str
    price: float
    number: int

    class Settings:
        name = "product"
        validate_on_save = True