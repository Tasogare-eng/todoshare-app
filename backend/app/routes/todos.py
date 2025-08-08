from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import Optional
from app.models.todo import TodoCreate, TodoUpdate, TodoResponse, TodoListResponse, TodoStatus
from app.models.user import UserResponse
from app.services.todo_service import todo_service
from app.core.dependencies import get_current_active_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_data: TodoCreate,
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Create a new todo"""
    try:
        todo = await todo_service.create_todo(current_user.id, todo_data)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create todo"
            )
        return todo
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating todo: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("", response_model=TodoListResponse)
async def get_todos(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    status: Optional[TodoStatus] = None,
    sort_by: str = Query("created_at", pattern="^(created_at|due_date|priority|title)$"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    search: Optional[str] = None,
    priority: Optional[str] = None,
    category_ids: Optional[str] = None,
    due_date_from: Optional[str] = None,
    due_date_to: Optional[str] = None,
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Get todos for current user with pagination and filters"""
    try:
        # Parse category_ids if provided
        parsed_category_ids = None
        if category_ids:
            parsed_category_ids = [id.strip() for id in category_ids.split(',') if id.strip()]
        
        result = await todo_service.get_todos(
            user_id=current_user.id,
            page=page,
            per_page=per_page,
            status=status,
            sort_by=sort_by,
            sort_order=sort_order,
            search=search,
            priority=priority,
            category_ids=parsed_category_ids,
            due_date_from=due_date_from,
            due_date_to=due_date_to
        )
        return TodoListResponse(**result)
    except Exception as e:
        logger.error(f"Error getting todos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: str,
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Get a specific todo by ID"""
    try:
        todo = await todo_service.get_todo_by_id(todo_id, current_user.id)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found"
            )
        return todo
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting todo: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: str,
    todo_update: TodoUpdate,
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Update a todo"""
    try:
        todo = await todo_service.update_todo(todo_id, current_user.id, todo_update)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found"
            )
        return todo
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating todo: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: str,
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Delete a todo"""
    try:
        success = await todo_service.delete_todo(todo_id, current_user.id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found"
            )
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting todo: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.patch("/{todo_id}/toggle", response_model=TodoResponse)
async def toggle_todo_status(
    todo_id: str,
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Toggle todo status between pending and completed"""
    try:
        todo = await todo_service.toggle_todo_status(todo_id, current_user.id)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found"
            )
        return todo
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error toggling todo status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )