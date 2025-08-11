from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, or_
from app.models.todo import TodoCreate, TodoUpdate, TodoResponse, TodoInDB, TodoStatus
from app.models.db_models import Todo, Category
from datetime import datetime
import uuid
import logging
import math

logger = logging.getLogger(__name__)

class TodoService:
    def __init__(self):
        pass
    
    async def create_todo(self, user_id: str, todo_data: TodoCreate, db: Session) -> Optional[TodoResponse]:
        """Create a new todo"""
        try:
            # Convert status to completed boolean for database
            completed = todo_data.status == TodoStatus.completed if todo_data.status else False
            
            db_todo = Todo(
                title=todo_data.title,
                description=todo_data.description,
                completed=completed,
                priority=todo_data.priority,
                due_date=todo_data.due_date,
                user_id=user_id,
                category_id=getattr(todo_data, 'category_id', None)
            )
            
            db.add(db_todo)
            db.commit()
            db.refresh(db_todo)
            
            # Convert back to TodoResponse format
            return TodoResponse(
                id=db_todo.id,
                title=db_todo.title,
                description=db_todo.description,
                status=TodoStatus.completed if db_todo.completed else TodoStatus.pending,
                priority=db_todo.priority,
                due_date=db_todo.due_date,
                user_id=db_todo.user_id,
                created_at=db_todo.created_at,
                updated_at=db_todo.updated_at
            )
            
        except Exception as e:
            logger.error(f"Error creating todo: {e}")
            db.rollback()
            return None
    
    async def get_todos(
        self, 
        user_id: str,
        db: Session,
        page: int = 1,
        per_page: int = 20,
        status: Optional[TodoStatus] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        search: Optional[str] = None,
        priority: Optional[str] = None,
        category_ids: Optional[List[str]] = None,
        due_date_from: Optional[str] = None,
        due_date_to: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get todos for a user with pagination"""
        try:
            # Start with base query
            query = db.query(Todo).filter(Todo.user_id == user_id)
            
            # Apply filters
            if status:
                completed = status == TodoStatus.completed
                query = query.filter(Todo.completed == completed)
            
            if search:
                search_filter = or_(
                    Todo.title.ilike(f"%{search}%"),
                    Todo.description.ilike(f"%{search}%")
                )
                query = query.filter(search_filter)
            
            if priority:
                query = query.filter(Todo.priority == priority)
            
            if category_ids:
                query = query.filter(Todo.category_id.in_(category_ids))
            
            # Date range filtering
            if due_date_from:
                from_date = datetime.fromisoformat(due_date_from.replace('Z', '+00:00'))
                query = query.filter(Todo.due_date >= from_date)
            
            if due_date_to:
                to_date = datetime.fromisoformat(due_date_to.replace('Z', '+00:00'))
                query = query.filter(Todo.due_date <= to_date)
            
            # Apply sorting
            if sort_by == "created_at":
                order_func = desc if sort_order == "desc" else asc
                query = query.order_by(order_func(Todo.created_at))
            elif sort_by == "due_date":
                order_func = desc if sort_order == "desc" else asc
                query = query.order_by(order_func(Todo.due_date))
            elif sort_by == "priority":
                # Custom priority ordering
                priority_case = {
                    "high": 3,
                    "medium": 2, 
                    "low": 1
                }
                if sort_order == "desc":
                    query = query.order_by(Todo.priority.desc())
                else:
                    query = query.order_by(Todo.priority.asc())
            
            # Get total count
            total = query.count()
            
            # Apply pagination
            offset = (page - 1) * per_page
            todos = query.offset(offset).limit(per_page).all()
            
            # Convert to response format
            todo_responses = []
            for todo in todos:
                todo_responses.append(TodoResponse(
                    id=todo.id,
                    title=todo.title,
                    description=todo.description,
                    status=TodoStatus.completed if todo.completed else TodoStatus.pending,
                    priority=todo.priority,
                    due_date=todo.due_date,
                    user_id=todo.user_id,
                    created_at=todo.created_at,
                    updated_at=todo.updated_at
                ))
            
            return {
                "items": todo_responses,
                "total": total,
                "page": page,
                "per_page": per_page,
                "pages": math.ceil(total / per_page) if total > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"Error getting todos: {e}")
            return {
                "items": [],
                "total": 0,
                "page": page,
                "per_page": per_page,
                "pages": 0
            }
    
    async def get_todo_by_id(self, todo_id: str, user_id: str, db: Session) -> Optional[TodoResponse]:
        """Get a specific todo by ID"""
        try:
            todo = db.query(Todo).filter(
                Todo.id == todo_id,
                Todo.user_id == user_id
            ).first()
            
            if todo:
                return TodoResponse(
                    id=todo.id,
                    title=todo.title,
                    description=todo.description,
                    status=TodoStatus.completed if todo.completed else TodoStatus.pending,
                    priority=todo.priority,
                    due_date=todo.due_date,
                    user_id=todo.user_id,
                    created_at=todo.created_at,
                    updated_at=todo.updated_at
                )
            return None
            
        except Exception as e:
            logger.error(f"Error getting todo: {e}")
            return None
    
    async def update_todo(
        self, 
        todo_id: str, 
        user_id: str, 
        todo_update: TodoUpdate,
        db: Session
    ) -> Optional[TodoResponse]:
        """Update a todo"""
        try:
            todo = db.query(Todo).filter(
                Todo.id == todo_id,
                Todo.user_id == user_id
            ).first()
            
            if not todo:
                return None
            
            # Update fields
            update_data = todo_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                if field == "status":
                    # Convert status to completed boolean
                    todo.completed = (value == TodoStatus.completed)
                else:
                    setattr(todo, field, value)
            
            db.commit()
            db.refresh(todo)
            
            return TodoResponse(
                id=todo.id,
                title=todo.title,
                description=todo.description,
                status=TodoStatus.completed if todo.completed else TodoStatus.pending,
                priority=todo.priority,
                due_date=todo.due_date,
                user_id=todo.user_id,
                created_at=todo.created_at,
                updated_at=todo.updated_at
            )
            
        except Exception as e:
            logger.error(f"Error updating todo: {e}")
            db.rollback()
            return None
    
    async def delete_todo(self, todo_id: str, user_id: str, db: Session) -> bool:
        """Delete a todo"""
        try:
            todo = db.query(Todo).filter(
                Todo.id == todo_id,
                Todo.user_id == user_id
            ).first()
            
            if not todo:
                return False
            
            db.delete(todo)
            db.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error deleting todo: {e}")
            db.rollback()
            return False
    
    async def toggle_todo_status(self, todo_id: str, user_id: str, db: Session) -> Optional[TodoResponse]:
        """Toggle todo status between pending and completed"""
        try:
            todo = db.query(Todo).filter(
                Todo.id == todo_id,
                Todo.user_id == user_id
            ).first()
            
            if not todo:
                return None
            
            # Toggle completed status
            todo.completed = not todo.completed
            db.commit()
            db.refresh(todo)
            
            return TodoResponse(
                id=todo.id,
                title=todo.title,
                description=todo.description,
                status=TodoStatus.completed if todo.completed else TodoStatus.pending,
                priority=todo.priority,
                due_date=todo.due_date,
                user_id=todo.user_id,
                created_at=todo.created_at,
                updated_at=todo.updated_at
            )
            
        except Exception as e:
            logger.error(f"Error toggling todo status: {e}")
            db.rollback()
            return None

# Singleton instance
todo_service = TodoService()