import httpx


def create_shared_async_client() -> httpx.AsyncClient:
    """Cliente HTTP async compartido (p. ej. gateway al microservicio de posts)."""
    return httpx.AsyncClient(timeout=30.0)
