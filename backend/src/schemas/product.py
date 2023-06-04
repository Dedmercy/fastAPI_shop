from typing import Optional

from pydantic import BaseModel


class CreateProductBase(BaseModel):
    name: str
    description: Optional[str]
    category: str
    price: float
    number: int


class UpdateProductBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
    category: Optional[str]
    price: Optional[float]
    number: Optional[int]
