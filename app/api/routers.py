from fastapi import APIRouter
from app.api.endpoints import recycle, community

api_router = APIRouter()
api_router.include_router(recycle.router, prefix="/recycle", tags=["recycle"])
api_router.include_router(community.router, prefix="/community", tags=["community"])
