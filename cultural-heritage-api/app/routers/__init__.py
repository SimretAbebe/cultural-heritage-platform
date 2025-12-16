from .auth import router as auth
from .users import router as users
from .categories import router as categories
from .heritage import router as heritage

# Export all routers
__all__ = ["auth", "users", "categories", "heritage"]
