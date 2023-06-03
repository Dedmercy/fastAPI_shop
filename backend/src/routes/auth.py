from fastapi import APIRouter

router = APIRouter(
    prefix="",
    tags=["Authorisation"]
)


@router.get("/auth")
async def authorisation():
    pass
