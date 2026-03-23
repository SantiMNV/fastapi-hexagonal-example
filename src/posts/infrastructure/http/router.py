from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.posts.domain.exceptions import (
    PostAuthorNotFoundException,
    PostNotFoundException,
)
from src.posts.infrastructure.http.requests import CreatePostRequest
from src.posts.infrastructure.http.responses import PostResponse
from src.shared.infrastructure.http import RequestContext, get_request_context

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/by-user/{user_id}", response_model=list[PostResponse])
def list_posts_for_user(
    user_id: str,
    ctx: RequestContext = Depends(get_request_context),
) -> list[PostResponse]:
    try:
        posts = ctx.factory.posts.create_list_user_posts_use_case().execute(user_id)
        return [PostResponse.model_validate(post) for post in posts]
    except PostAuthorNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc


@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    payload: CreatePostRequest,
    ctx: RequestContext = Depends(get_request_context),
) -> PostResponse:
    try:
        post = ctx.factory.posts.create_create_post_use_case().execute(
            user_id=payload.user_id,
            title=payload.title,
            content=payload.content,
        )
        return PostResponse.model_validate(post)
    except PostAuthorNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc


@router.get("/{post_id}", response_model=PostResponse)
def get_post(
    post_id: str,
    ctx: RequestContext = Depends(get_request_context),
) -> PostResponse:
    try:
        post = ctx.factory.posts.create_get_post_use_case().execute(post_id)
        return PostResponse.model_validate(post)
    except PostNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: str,
    ctx: RequestContext = Depends(get_request_context),
) -> Response:
    try:
        ctx.factory.posts.create_delete_post_use_case().execute(post_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except PostNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc
