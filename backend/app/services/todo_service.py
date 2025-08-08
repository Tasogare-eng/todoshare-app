from typing import Optional, List, Dict, Any
from app.models.todo import TodoCreate, TodoUpdate, TodoResponse, TodoInDB, TodoStatus
from datetime import datetime
import uuid
import logging
import math

logger = logging.getLogger(__name__)

# In-memory storage for development
mock_todos: Dict[str, TodoInDB] = {}

class TodoService:
    def __init__(self):
        # Using mock storage only - no external database
        pass
    
    async def create_todo(self, user_id: str, todo_data: TodoCreate) -> Optional[TodoResponse]:
        """Create a new todo"""
        try:
            todo_id = str(uuid.uuid4())
            now = datetime.utcnow()
            
            todo = TodoInDB(
                id=todo_id,
                user_id=user_id,
                title=todo_data.title,
                description=todo_data.description,
                status=todo_data.status,
                priority=todo_data.priority,
                due_date=todo_data.due_date,
                created_at=now,
                updated_at=None
            )
            mock_todos[todo_id] = todo
            return TodoResponse(**todo.model_dump())
            
        except Exception as e:
            logger.error(f"Error creating todo: {e}")
            return None
    
    async def get_todos(
        self, 
        user_id: str,
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
            # Filter mock todos by user
            user_todos = [
                todo for todo in mock_todos.values() 
                if todo.user_id == user_id
            ]
            
            # Apply filters
            if status:
                user_todos = [
                    todo for todo in user_todos 
                    if todo.status == status
                ]
            
            if search:
                search_lower = search.lower()
                user_todos = [
                    todo for todo in user_todos
                    if search_lower in todo.title.lower() or
                    (todo.description and search_lower in todo.description.lower())
                ]
            
            if priority:
                user_todos = [
                    todo for todo in user_todos
                    if todo.priority and todo.priority.value == priority
                ]
            
            # Date range filtering
            if due_date_from or due_date_to:
                if due_date_from:
                    from_date = datetime.fromisoformat(due_date_from.replace('Z', '+00:00'))
                    user_todos = [
                        todo for todo in user_todos
                        if todo.due_date and todo.due_date >= from_date
                    ]
                if due_date_to:
                    to_date = datetime.fromisoformat(due_date_to.replace('Z', '+00:00'))
                    user_todos = [
                        todo for todo in user_todos
                        if todo.due_date and todo.due_date <= to_date
                    ]
            
            # Sort todos
            reverse = (sort_order == "desc")
            if sort_by == "created_at":
                user_todos.sort(key=lambda x: x.created_at, reverse=reverse)
            elif sort_by == "due_date":
                user_todos.sort(key=lambda x: x.due_date or datetime.max, reverse=reverse)
            elif sort_by == "priority":
                priority_order = {"high": 3, "medium": 2, "low": 1}
                user_todos.sort(
                    key=lambda x: priority_order.get(x.priority.value if x.priority else "medium", 2),
                    reverse=reverse
                )
            
            # Paginate
            total = len(user_todos)
            start = (page - 1) * per_page
            end = start + per_page
            paginated_todos = user_todos[start:end]
            
            return {
                "items": [TodoResponse(**todo.model_dump()) for todo in paginated_todos],
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
    
    async def get_todo_by_id(self, todo_id: str, user_id: str) -> Optional[TodoResponse]:
        """Get a specific todo by ID"""
        try:
            todo = mock_todos.get(todo_id)
            if todo and todo.user_id == user_id:
                return TodoResponse(**todo.model_dump())
            return None
            
        except Exception as e:
            logger.error(f"Error getting todo: {e}")
            return None
    
    async def update_todo(
        self, 
        todo_id: str, 
        user_id: str, 
        todo_update: TodoUpdate
    ) -> Optional[TodoResponse]:
        """Update a todo"""
        try:
            todo = mock_todos.get(todo_id)
            if todo and todo.user_id == user_id:
                # Update fields
                update_data = todo_update.model_dump(exclude_unset=True)
                for field, value in update_data.items():
                    setattr(todo, field, value)
                todo.updated_at = datetime.utcnow()
                mock_todos[todo_id] = todo
                return TodoResponse(**todo.model_dump())
            return None
            
        except Exception as e:
            logger.error(f"Error updating todo: {e}")
            return None
    
    async def delete_todo(self, todo_id: str, user_id: str) -> bool:
        """Delete a todo"""
        try:
            if todo_id in mock_todos and mock_todos[todo_id].user_id == user_id:
                del mock_todos[todo_id]
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error deleting todo: {e}")
            return False
    
    async def toggle_todo_status(self, todo_id: str, user_id: str) -> Optional[TodoResponse]:
        """Toggle todo status between pending and completed"""
        try:
            # Get the todo
            todo = await self.get_todo_by_id(todo_id, user_id)
            if not todo:
                return None
            
            # Toggle status
            new_status = TodoStatus.COMPLETED if todo.status == TodoStatus.PENDING else TodoStatus.PENDING
            
            # Update the todo
            update_data = TodoUpdate(status=new_status)
            return await self.update_todo(todo_id, user_id, update_data)
            
        except Exception as e:
            logger.error(f"Error toggling todo status: {e}")
            return None

# Singleton instance
todo_service = TodoService()