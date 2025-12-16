from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from fastapi import APIRouter, Depends, HTTPException, status, Query
from math import ceil

from app.database import get_db
from app import models
from app.schemas import (
    HeritageEntryCreate, HeritageEntryResponse, HeritageEntryDetailResponse,
    PaginatedResponse, HeritageSearchParams
)
from app.utils.dependencies import get_current_admin_user

# Create the heritage router
router = APIRouter()

@router.get("/", response_model=PaginatedResponse)
async def get_heritage_entries(
    page: int = Query(1, ge=1, description="Page number (1-based)"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    search: str = Query(None, description="Search keyword in title or content"),
    category_id: int = Query(None, description="Filter by category ID"),
    db: Session = Depends(get_db)
):
    
    # Build base query
    query = db.query(
        models.HeritageEntry,
        models.Category.name.label('category_name'),
        models.User.username.label('creator_username')
    ).join(
        models.Category, models.HeritageEntry.category_id == models.Category.id
    ).join(
        models.User, models.HeritageEntry.created_by == models.User.id
    )

    # Apply search filter if provided
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                models.HeritageEntry.title.ilike(search_term),
                models.HeritageEntry.content.ilike(search_term)
            )
        )

    # Apply category filter if provided
    if category_id is not None:
        query = query.filter(models.HeritageEntry.category_id == category_id)

    # Get total count for pagination
    total = query.count()

    # Apply pagination
    items = query.offset((page - 1) * size).limit(size).all()

    # Calculate pagination metadata
    pages = ceil(total / size) if total > 0 else 1

    # Convert to response format
    heritage_items = []
    for item in items:
        entry, category_name, creator_username = item
        heritage_items.append(HeritageEntryResponse(
            id=entry.id,
            title=entry.title,
            content=entry.content,
            category_id=entry.category_id,
            created_by=entry.created_by,
            created_at=entry.created_at,
            category_name=category_name,
            creator_username=creator_username
        ))

    return PaginatedResponse(
        items=heritage_items,
        total=total,
        page=page,
        size=size,
        pages=pages
    )

@router.get("/{heritage_id}", response_model=HeritageEntryDetailResponse)
async def get_heritage_entry(heritage_id: int, db: Session = Depends(get_db)):
   
    # Query with joins to get related data
    result = db.query(
        models.HeritageEntry,
        models.Category.name.label('category_name'),
        models.User.username.label('creator_username')
    ).join(
        models.Category, models.HeritageEntry.category_id == models.Category.id
    ).join(
        models.User, models.HeritageEntry.created_by == models.User.id
    ).filter(
        models.HeritageEntry.id == heritage_id
    ).first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Heritage entry not found"
        )

    entry, category_name, creator_username = result

    return HeritageEntryDetailResponse(
        id=entry.id,
        title=entry.title,
        content=entry.content,
        category_id=entry.category_id,
        created_by=entry.created_by,
        created_at=entry.created_at,
        category_name=category_name,
        creator_username=creator_username
    )

@router.post("/", response_model=HeritageEntryResponse)
async def create_heritage_entry(
    entry_data: HeritageEntryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
  
    # Verify category exists
    category = db.query(models.Category).filter(
        models.Category.id == entry_data.category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid category ID"
        )

    # Create new heritage entry
    db_entry = models.HeritageEntry(
        title=entry_data.title,
        content=entry_data.content,
        category_id=entry_data.category_id,
        created_by=current_user.id
    )

    # Save to database
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)

    # Return with additional metadata
    return HeritageEntryResponse(
        id=db_entry.id,
        title=db_entry.title,
        content=db_entry.content,
        category_id=db_entry.category_id,
        created_by=db_entry.created_by,
        created_at=db_entry.created_at,
        category_name=category.name,
        creator_username=current_user.username
    )
