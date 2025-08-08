from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum

class TodoStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class TodoPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"

class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: TodoStatus = TodoStatus.PENDING
    priority: Optional[TodoPriority] = TodoPriority.MEDIUM
    due_date: Optional[datetime] = None
    category_ids: Optional[List[str]] = []

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: Optional[TodoStatus] = None
    priority: Optional[TodoPriority] = None
    due_date: Optional[datetime] = None
    category_ids: Optional[List[str]] = None

class TodoResponse(TodoBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    categories: Optional[List[dict]] = []

class TodoInDB(TodoBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    categories: Optional[List[dict]] = []

class TodoListResponse(BaseModel):
    items: list[TodoResponse]
    total: int
    page: int
    per_page: int
    pages: int