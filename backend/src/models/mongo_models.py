from typing import List, Optional


from beanie import Document, Indexed, Link


class Product(Document):
    name: str
    description: Optional[str]
    category: str
    price: float
    number: int

    class Settings:
        name = "product"
        validate_on_save = True


# class Cart(Document):
#     _id: int
#     products: List[Link[Product]]
#
#     class Settings:
#         name = 'cart'
#         validate_on_save = True
