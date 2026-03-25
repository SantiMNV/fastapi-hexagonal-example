from fastapi import APIRouter, Depends, Response, status

from src.posts.infrastructure.http.responses import PostResponse
from src.shared.infrastructure.http import RequestContext, get_request_context
from src.shared.infrastructure.http.internal_auth import verify_internal_api_key

router = APIRouter(
    prefix="/internal/posts",
    tags=["internal"],
    dependencies=[Depends(verify_internal_api_key)],
)


@router.get("", response_model=list[PostResponse])
async def get_posts_by_user(
    user_id: str,
    ctx: RequestContext = Depends(get_request_context),
) -> list[PostResponse]:
    posts = await ctx.factory.posts.create_get_posts_by_user_use_case().execute(user_id)
    return [PostResponse.model_validate(post) for post in posts]


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_posts(
    user_id: str,
    ctx: RequestContext = Depends(get_request_context),
) -> Response:
    await ctx.factory.posts.create_delete_user_posts_use_case().execute(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
