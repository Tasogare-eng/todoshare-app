from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
import uuid

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_active: bool = True
    
class UserInDB(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    hashed_password: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_active: bool = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenData(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None