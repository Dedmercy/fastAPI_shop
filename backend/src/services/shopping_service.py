from fastapi import HTTPException

from bson import ObjectId


class ShoppingService:

    @staticmethod
    def verify_product_id(product_id: str):
        if ObjectId.is_valid(product_id):
            return
        raise HTTPException(
            status_code=400,
            detail=f"ID:{product_id} is not valid ObjectId, it must be a 12-byte input or a 24-character hex string"
        )

    @staticmethod
    def get_cart(id_: int):
        ShoppingService.verify_product_id()
