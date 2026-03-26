from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.posts.domain.eligibility import PostAuthorEligibilityReason
from src.posts.domain.exceptions import (
    PostAuthorNotEligibleException,
    PostNotFoundException,
)
from src.posts.infrastructure.http.requests import CreatePostRequest
from src.posts.infrastructure.http.responses import PostResponse
from src.shared.infrastructure.http import RequestContext, get_request_context

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    payload: CreatePostRequest,
    ctx: RequestContext = Depends(get_request_context),
) -> PostResponse:
    try:
        post = await ctx.factory.posts.create_create_post_use_case().execute(
            user_id=payload.user_id,
            title=payload.title,
            content=payload.content,
        )
        return PostResponse.model_validate(post)
    except PostAuthorNotEligibleException as exc:
        if exc.eligibility_reason == PostAuthorEligibilityReason.NOT_FOUND:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=exc.message) from exc


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: str,
    ctx: RequestContext = Depends(get_request_context),
) -> PostResponse:
    try:
        post = await ctx.factory.posts.create_get_post_use_case().execute(post_id)
        return PostResponse.model_validate(post)
    except PostNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: str,
    ctx: RequestContext = Depends(get_request_context),
) -> Response:
    try:
        await ctx.factory.posts.create_delete_post_use_case().execute(post_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except PostNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc
