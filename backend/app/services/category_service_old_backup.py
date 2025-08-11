import uuid
from datetime import datetime
from typing import Optional, List, Dict
from app.models.category import (
    CategoryCreate, 
    CategoryUpdate, 
    CategoryResponse, 
    CategoryInDB,
    mock_categories,
    default_categories
)


class CategoryService:
    def __init__(self):
        self.categories = mock_categories
    
    async def create_user_default_categories(self, user_id: str) -> List[CategoryInDB]:
        """Create default categories for a new user"""
        categories = []
        for default_cat in default_categories:
            category_data = CategoryCreate(**default_cat)
            category = await self.create_category(user_id, category_data)
            if category:
                categories.append(category)
        return categories
    
    async def create_category(self, user_id: str, category_data: CategoryCreate) -> Optional[CategoryInDB]:
        """Create a new category"""
        try:
            # Check for duplicate name within user's categories
            user_categories = await self.get_categories_by_user(user_id)
            if any(cat.name == category_data.name for cat in user_categories):
                return None  # Duplicate name
            
            category_id = str(uuid.uuid4())
            now = datetime.utcnow()
            
            category = CategoryInDB(
                id=category_id,
                user_id=user_id,
                name=category_data.name,
                color=category_data.color or "#007bff",
                description=category_data.description,
                created_at=now,
                updated_at=None,
                todo_count=0
            )
            
            self.categories[category_id] = category
            return category
        except Exception as e:
            print(f"Error creating category: {e}")
            return None
    
    async def get_categories_by_user(self, user_id: str) -> List[CategoryInDB]:
        """Get all categories for a user"""
        user_categories = [
            category for category in self.categories.values() 
            if category.user_id == user_id
        ]
        return sorted(user_categories, key=lambda x: x.created_at)
    
    async def get_category_by_id(self, category_id: str, user_id: str) -> Optional[CategoryInDB]:
        """Get a specific category by ID"""
        category = self.categories.get(category_id)
        if category and category.user_id == user_id:
            return category
        return None
    
    async def update_category(self, category_id: str, user_id: str, update_data: CategoryUpdate) -> Optional[CategoryInDB]:
        """Update a category"""
        try:
            category = await self.get_category_by_id(category_id, user_id)
            if not category:
                return None
            
            # Check for duplicate name if name is being updated
            if update_data.name and update_data.name != category.name:
                user_categories = await self.get_categories_by_user(user_id)
                if any(cat.name == update_data.name and cat.id != category_id for cat in user_categories):
                    return None  # Duplicate name
            
            # Update fields
            update_dict = update_data.model_dump(exclude_unset=True)
            for field, value in update_dict.items():
                setattr(category, field, value)
            
            category.updated_at = datetime.utcnow()
            self.categories[category_id] = category
            
            return category
        except Exception as e:
            print(f"Error updating category: {e}")
            return None
    
    async def delete_category(self, category_id: str, user_id: str) -> bool:
        """Delete a category"""
        try:
            category = await self.get_category_by_id(category_id, user_id)
            if not category:
                return False
            
            # TODO: Remove category from all todos that use it
            # For now, we'll just delete the category
            del self.categories[category_id]
            return True
        except Exception as e:
            print(f"Error deleting category: {e}")
            return False
    
    async def update_category_todo_count(self, category_id: str):
        """Update the todo count for a category"""
        # This will be implemented when we have the todo-category relationship
        pass


# Global service instance
category_service = CategoryService()