"""
Pydantic schemas for User data validation and serialization.
- UserCreate: what a client sends when registering (includes plain password).
- UserRead:   what the API returns (never includes password_hash).
"""
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict
class UserCreate(BaseModel):
    """Schema for creating a new user. Validates incoming registration data."""
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
class UserRead(BaseModel):
    """Schema for returning user data. Excludes password_hash entirely."""
    model_config = ConfigDict(from_attributes=True)
    id: int

    username: str
    email: EmailStr
    created_at: datetime
