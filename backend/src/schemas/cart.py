from pydantic import BaseModel
from typing import Optional


class CartSchema(BaseModel):
    account_id: int
    product_id: str
    amount: int


class UpdateCartSchema(BaseModel):
    product_id: str
    amount: int
