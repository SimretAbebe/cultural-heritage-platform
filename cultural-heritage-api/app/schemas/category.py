from typing import Optional
from pydantic import BaseModel

class CategoryBase(BaseModel):
    """Base category schema with common fields."""
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    """Schema for category creation requests."""
    pass  # All fields are optional in base

class CategoryUpdate(BaseModel):
    """Schema for category update requests."""
    name: Optional[str] = None
    description: Optional[str] = None

class CategoryResponse(CategoryBase):
    """Schema for category response data."""
    id: int

    class Config:
        """Pydantic configuration for ORM compatibility."""
        from_attributes = True
