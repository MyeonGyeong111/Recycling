from fastapi import APIRouter
from app.schemas.community import PostCreate, PostResponse
from app.services.community_service import CommunityService

router = APIRouter()

@router.get("/posts", response_model=list[PostResponse])
async def get_posts():
    """
    Returns all community posts.
    """
    return CommunityService.get_all_posts()

@router.post("/posts", response_model=PostResponse)
async def create_new_post(post: PostCreate):
    """
    Creates a new community post.
    """
    return CommunityService.create_post(post.model_dump())
