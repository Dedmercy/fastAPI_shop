from fastapi import APIRouter

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.get("/all")
async def get_all_products():
    pass