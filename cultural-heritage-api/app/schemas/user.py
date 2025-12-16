from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    """Base user schema with common fields."""
    username: str
    email: EmailStr

class UserCreate(UserBase):
    """Schema for user registration requests."""
    username: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    """Schema for user update requests."""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    """Schema for user response data."""
    id: int
    role: str
    created_at: datetime

    class Config:
        """Pydantic configuration for ORM compatibility."""
        from_attributes = True

class UserLogin(BaseModel):
    """Schema for login requests."""
    username: str
    password: str

class Token(BaseModel):
    """Schema for JWT token responses."""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Schema for token payload data."""
    username: Optional[str] = None
