"""Shared-secret auth for service-to-service ``/internal/*`` routes."""

from __future__ import annotations

import hashlib
import hmac
import logging

from fastapi import HTTPException, Request, status

from src.shared.infrastructure.settings import get_settings

logger = logging.getLogger(__name__)


def _constant_time_token_equal(expected: str, provided: str | None) -> bool:
    """Compare API key material without leaking length differences via timing."""
    if provided is None:
        provided = ""
    return hmac.compare_digest(
        hashlib.sha256(expected.encode("utf-8")).digest(),
        hashlib.sha256(provided.encode("utf-8")).digest(),
    )


async def verify_internal_api_key(request: Request) -> None:
    settings = get_settings()
    configured = settings.internal_api_key
    if not configured or not configured.strip():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Internal API is not configured",
        )
    token = request.headers.get(settings.internal_api_header_name)
    if not _constant_time_token_equal(configured, token):
        client = request.client
        logger.warning(
            "internal API auth failed",
            extra={
                "path": request.url.path,
                "client_host": client.host if client else None,
            },
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing internal credentials",
        )
