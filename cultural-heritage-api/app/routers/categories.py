from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from app.database import get_db
from app import models
from app.schemas import CategoryCreate, CategoryResponse
from app.utils.dependencies import get_current_admin_user

# Create the categories router
router = APIRouter()

@router.get("/", response_model=List[CategoryResponse])
async def get_categories(db: Session = Depends(get_db)):
  
    categories = db.query(models.Category).all()
    return categories

@router.post("/", response_model=CategoryResponse)
async def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
   
    # Check if category name already exists
    existing_category = db.query(models.Category).filter(
        models.Category.name == category_data.name
    ).first()

    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists"
        )

    # Create new category
    db_category = models.Category(
        name=category_data.name,
        description=category_data.description
    )

    # Save to database
    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return db_category

@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, db: Session = Depends(get_db)):
   
    category = db.query(models.Category).filter(
        models.Category.id == category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    return category
