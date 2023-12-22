from fastapi import APIRouter

from api.api_v1.endpoints import users, images


api_router = APIRouter()
# api_router.include_router(login.router, tags=["login"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(users.router, prefix="/v1/users", tags=["user"])
api_router.include_router(images.router, prefix="/v1/images", tags=["images"])
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])
