from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId

from src.repository.products_repo import ProductRepository
from src.schemas.product import CreateProductBase, UpdateProductBase
from src.auth.jwt import JWTRepository

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/all")
async def get_all_products():
    result = await ProductRepository.get_all()
    return {"products": result}


@router.post("/create")
async def create_product(obj_in: CreateProductBase, auth: dict = Depends(JWTRepository.check_admin)):
    result = await ProductRepository.create(obj_in)
    return {"created_product": result}


@router.get('/by_id')
async def get_product_by_id(id_: str):

    if not ObjectId.is_valid(id_):
        raise HTTPException(
            status_code=400,
            detail=f"ID:{id_} is not valid ObjectId, it must be a 12-byte input or a 24-character hex string"
        )

    result = await ProductRepository.get_by_id(id_)

    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Product with ID:{id_} is not exist"
        )

    return {"product_info": result}


@router.put('/update')
async def update_product(obj_in: UpdateProductBase, id_: str, auth: dict = Depends(JWTRepository.check_admin)):

    if not ObjectId.is_valid(id_):
        raise HTTPException(
            status_code=400,
            detail=f"ID:{id_} is not valid ObjectId, it must be a 12-byte input or a 24-character hex string"
        )

    if not (await ProductRepository.get_by_id(id_)):
        raise HTTPException(
            status_code=404,
            detail=f"Product with ID:{id_} is not exist"
        )

    updated_product = await ProductRepository.update(obj_in, id_)

    return {"updated_product": updated_product}


@router.delete('/delete')
async def delete_product(id_: str, auth: dict = Depends(JWTRepository.check_admin)):

    if not ObjectId.is_valid(id_):
        raise HTTPException(
            status_code=400,
            detail=f"ID:{id_} is not valid ObjectId, it must be a 12-byte input or a 24-character hex string"
        )

    if not (await ProductRepository.get_by_id(id_)):
        raise HTTPException(
            status_code=404,
            detail=f"Product with ID:{id_} is not exist"
        )

    deleted_product = await ProductRepository.delete(id_)
    return {"deleted_product": deleted_product}
