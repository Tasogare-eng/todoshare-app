from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=30)
    color: Optional[str] = Field(default="#007bff", pattern="^#[0-9A-Fa-f]{6}$")
    description: Optional[str] = Field(default=None, max_length=200)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=30)
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")
    description: Optional[str] = Field(None, max_length=200)


class CategoryResponse(CategoryBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime]
    todo_count: Optional[int] = 0

    class Config:
        from_attributes = True


class CategoryListResponse(BaseModel):
    items: List[CategoryResponse]
    total: int


# In-memory storage for development
class CategoryInDB(CategoryResponse):
    pass


# Mock storage for categories
mock_categories: dict[str, CategoryInDB] = {}


# Default categories
default_categories = [
    {
        "name": "仕事",
        "color": "#1976d2",
        "description": "業務関連のタスク"
    },
    {
        "name": "プライベート", 
        "color": "#388e3c",
        "description": "個人的なタスク"
    },
    {
        "name": "買い物",
        "color": "#f57c00",
        "description": "購入予定の商品"
    },
    {
        "name": "その他",
        "color": "#7b1fa2",
        "description": "未分類のタスク"
    }
]