import uuid
from datetime import datetime
from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.category import (
    CategoryCreate, 
    CategoryUpdate, 
    CategoryResponse, 
    CategoryInDB,
    default_categories
)
from app.models.db_models import Category, Todo


class CategoryService:
    def __init__(self):
        pass
    
    async def create_user_default_categories(self, user_id: str, db: Session) -> List[CategoryResponse]:
        """Create default categories for a new user"""
        categories = []
        for default_cat in default_categories:
            category_data = CategoryCreate(**default_cat)
            category = await self.create_category(user_id, category_data, db)
            if category:
                categories.append(category)
        return categories
    
    async def create_category(self, user_id: str, category_data: CategoryCreate, db: Session) -> Optional[CategoryResponse]:
        """Create a new category"""
        try:
            # Check for duplicate name within user's categories
            existing = db.query(Category).filter(
                Category.user_id == user_id,
                Category.name == category_data.name
            ).first()
            
            if existing:
                return None  # Duplicate name
            
            db_category = Category(
                user_id=user_id,
                name=category_data.name,
                color=category_data.color or "#6B7280"
            )
            
            db.add(db_category)
            db.commit()
            db.refresh(db_category)
            
            # Get todo count for this category
            todo_count = db.query(Todo).filter(Todo.category_id == db_category.id).count()
            
            return CategoryResponse(
                id=db_category.id,
                name=db_category.name,
                color=db_category.color,
                user_id=db_category.user_id,
                created_at=db_category.created_at,
                updated_at=db_category.updated_at,
                todo_count=todo_count
            )
            
        except Exception as e:
            print(f"Error creating category: {e}")
            db.rollback()
            return None
    
    async def get_categories_by_user(self, user_id: str, db: Session) -> List[CategoryResponse]:
        """Get all categories for a user"""
        try:
            # Get categories with todo counts
            categories_query = db.query(
                Category,
                func.count(Todo.id).label('todo_count')
            ).outerjoin(
                Todo, Category.id == Todo.category_id
            ).filter(
                Category.user_id == user_id
            ).group_by(Category.id).all()
            
            categories = []
            for category, todo_count in categories_query:
                categories.append(CategoryResponse(
                    id=category.id,
                    name=category.name,
                    color=category.color,
                    user_id=category.user_id,
                    created_at=category.created_at,
                    updated_at=category.updated_at,
                    todo_count=todo_count
                ))
            
            return categories
            
        except Exception as e:
            print(f"Error getting user categories: {e}")
            return []
    
    async def get_category_by_id(self, category_id: str, user_id: str, db: Session) -> Optional[CategoryResponse]:
        """Get a specific category by ID"""
        try:
            category = db.query(Category).filter(
                Category.id == category_id,
                Category.user_id == user_id
            ).first()
            
            if not category:
                return None
            
            # Get todo count
            todo_count = db.query(Todo).filter(Todo.category_id == category_id).count()
            
            return CategoryResponse(
                id=category.id,
                name=category.name,
                color=category.color,
                user_id=category.user_id,
                created_at=category.created_at,
                updated_at=category.updated_at,
                todo_count=todo_count
            )
            
        except Exception as e:
            print(f"Error getting category: {e}")
            return None
    
    async def update_category(
        self, 
        category_id: str, 
        user_id: str, 
        category_update: CategoryUpdate,
        db: Session
    ) -> Optional[CategoryResponse]:
        """Update a category"""
        try:
            category = db.query(Category).filter(
                Category.id == category_id,
                Category.user_id == user_id
            ).first()
            
            if not category:
                return None
            
            # Check for duplicate name if name is being updated
            update_data = category_update.model_dump(exclude_unset=True)
            if 'name' in update_data:
                existing = db.query(Category).filter(
                    Category.user_id == user_id,
                    Category.name == update_data['name'],
                    Category.id != category_id
                ).first()
                
                if existing:
                    return None  # Duplicate name
            
            # Update fields
            for field, value in update_data.items():
                setattr(category, field, value)
            
            db.commit()
            db.refresh(category)
            
            # Get todo count
            todo_count = db.query(Todo).filter(Todo.category_id == category_id).count()
            
            return CategoryResponse(
                id=category.id,
                name=category.name,
                color=category.color,
                user_id=category.user_id,
                created_at=category.created_at,
                updated_at=category.updated_at,
                todo_count=todo_count
            )
            
        except Exception as e:
            print(f"Error updating category: {e}")
            db.rollback()
            return None
    
    async def delete_category(self, category_id: str, user_id: str, db: Session) -> bool:
        """Delete a category"""
        try:
            category = db.query(Category).filter(
                Category.id == category_id,
                Category.user_id == user_id
            ).first()
            
            if not category:
                return False
            
            # Set todos in this category to have no category
            db.query(Todo).filter(Todo.category_id == category_id).update(
                {Todo.category_id: None}
            )
            
            # Delete the category
            db.delete(category)
            db.commit()
            return True
            
        except Exception as e:
            print(f"Error deleting category: {e}")
            db.rollback()
            return False


# Singleton instance
category_service = CategoryService()