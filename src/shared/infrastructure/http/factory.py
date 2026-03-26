"""Re-export composition root; implementation lives in `src.app.composition`."""

from src.app.composition.app_factory import AppFactory

__all__ = ["AppFactory"]
