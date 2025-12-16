from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class HeritageEntryBase(BaseModel):
    """Base heritage entry schema with common fields."""
    title: str
    content: str
    category_id: int

class HeritageEntryCreate(HeritageEntryBase):
    """Schema for heritage entry creation requests."""
    pass  # All fields are in base

class HeritageEntryUpdate(BaseModel):
    """Schema for heritage entry update requests."""
    title: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[int] = None

class HeritageEntryResponse(HeritageEntryBase):
    """Schema for heritage entry response data."""
    id: int
    created_by: int
    created_at: datetime
    category_name: Optional[str] = None  # Joined from category table
    creator_username: Optional[str] = None  # Joined from user table

    class Config:
        """Pydantic configuration for ORM compatibility."""
        from_attributes = True

class HeritageEntryDetailResponse(HeritageEntryResponse):
    """Detailed response including full category and creator information."""
    pass  # Extends HeritageEntryResponse

# Pagination schemas
class PaginationParams(BaseModel):
    """Schema for pagination query parameters."""
    page: int = 1
    size: int = 10

class HeritageSearchParams(PaginationParams):
    """Schema for heritage search and filtering parameters."""
    search: Optional[str] = None
    category_id: Optional[int] = None

class PaginatedResponse(BaseModel):
    """Generic paginated response wrapper."""
    items: List[HeritageEntryResponse]
    total: int
    page: int
    size: int
    pages: int
