from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.posts.infrastructure.http.responses import PostResponse
from src.shared.infrastructure.http import RequestContext, get_request_context
from src.users.domain.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
)
from src.users.infrastructure.http.requests import RegisterUserRequest
from src.users.infrastructure.http.responses import UserResponse, UserWithPostsResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: RegisterUserRequest,
    ctx: RequestContext = Depends(get_request_context),
) -> UserResponse:
    try:
        user = await ctx.factory.users.create_register_user_use_case().execute(
            name=payload.name,
            email=str(payload.email),
        )
        return UserResponse.model_validate(user)
    except UserAlreadyExistsException as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.message) from exc


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    ctx: RequestContext = Depends(get_request_context),
) -> UserResponse:
    try:
        user = await ctx.factory.users.create_get_user_use_case().execute(user_id)
        return UserResponse.model_validate(user)
    except UserNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    ctx: RequestContext = Depends(get_request_context),
) -> Response:
    try:
        await ctx.factory.users.create_delete_user_use_case().execute(user_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except UserNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc


@router.get("/{user_id}/posts", response_model=list[PostResponse])
async def get_user_posts(
    user_id: str,
    ctx: RequestContext = Depends(get_request_context),
) -> list[PostResponse]:
    try:
        posts = await ctx.factory.posts.create_list_user_posts_use_case().execute(user_id)
        return [PostResponse.model_validate(post) for post in posts]
    except UserNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc


@router.get("/{user_id}/with-posts", response_model=UserWithPostsResponse)
async def get_user_with_posts(
    user_id: str,
    ctx: RequestContext = Depends(get_request_context),
) -> UserWithPostsResponse:
    try:
        user, posts = await ctx.factory.users.create_get_user_with_posts_use_case().execute(
            user_id
        )
        return UserWithPostsResponse(
            user=UserResponse.model_validate(user),
            posts=[PostResponse.model_validate(p) for p in posts],
        )
    except UserNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc
