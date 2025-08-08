from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from app.models.category import CategoryCreate, CategoryUpdate, CategoryResponse, CategoryListResponse
from app.models.user import UserResponse
from app.services.category_service import category_service
from app.core.dependencies import get_current_active_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Create a new category"""
    try:
        category = await category_service.create_category(current_user.id, category_data)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this name already exists"
            )
        return CategoryResponse(**category.model_dump())
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating category: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("", response_model=CategoryListResponse)
async def get_categories(
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Get all categories for the current user"""
    try:
        categories = await category_service.get_categories_by_user(current_user.id)
        
        # If no categories exist, create default ones
        if not categories:
            categories = await category_service.create_user_default_categories(current_user.id)
        
        category_responses = [CategoryResponse(**cat.model_dump()) for cat in categories]
        return CategoryListResponse(
            items=category_responses,
            total=len(category_responses)
        )
    except Exception as e:
        logger.error(f"Error getting categories: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: str,
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Get a specific category by ID"""
    try:
        category = await category_service.get_category_by_id(category_id, current_user.id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        return CategoryResponse(**category.model_dump())
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting category: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: str,
    category_update: CategoryUpdate,
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Update a category"""
    try:
        category = await category_service.update_category(category_id, current_user.id, category_update)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found or name already exists"
            )
        return CategoryResponse(**category.model_dump())
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating category: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: str,
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Delete a category"""
    try:
        success = await category_service.delete_category(category_id, current_user.id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting category: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )