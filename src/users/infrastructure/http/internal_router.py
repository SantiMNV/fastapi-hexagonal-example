from fastapi import APIRouter, Depends, HTTPException, status

from src.shared.infrastructure.http import RequestContext, get_request_context
from src.shared.infrastructure.http.internal_auth import verify_internal_api_key
from src.users.domain.exceptions import UserNotFoundException
from src.users.infrastructure.http.responses import UserResponse

router = APIRouter(
    prefix="/internal/users",
    tags=["internal"],
    dependencies=[Depends(verify_internal_api_key)],
)


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
