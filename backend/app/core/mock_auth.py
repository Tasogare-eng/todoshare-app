"""
Mock authentication service for development without Supabase
"""
from typing import Dict, Optional
from app.models.user import UserInDB
from app.core.security import get_password_hash
from datetime import datetime
import uuid

# In-memory user storage for development
mock_users: Dict[str, UserInDB] = {}

def create_mock_user(email: str, username: str, password: str) -> UserInDB:
    """Create a mock user for development"""
    user_id = str(uuid.uuid4())
    hashed_password = get_password_hash(password)
    now = datetime.utcnow()
    
    user = UserInDB(
        id=user_id,
        email=email,
        username=username,
        hashed_password=hashed_password,
        created_at=now,
        is_active=True
    )
    
    # Store in mock database
    mock_users[email] = user
    return user

def get_mock_user_by_email(email: str) -> Optional[UserInDB]:
    """Get mock user by email"""
    return mock_users.get(email)

def get_mock_user_by_id(user_id: str) -> Optional[UserInDB]:
    """Get mock user by ID"""
    for user in mock_users.values():
        if user.id == user_id:
            return user
    return None

def create_mock_google_user(email: str, username: str, google_id: str, picture: str = "") -> UserInDB:
    """Create a mock user from Google OAuth for development"""
    user_id = str(uuid.uuid4())
    # For Google users, we don't have a password, so use a placeholder hash
    hashed_password = "google_oauth_user"
    now = datetime.utcnow()
    
    user = UserInDB(
        id=user_id,
        email=email,
        username=username,
        hashed_password=hashed_password,
        created_at=now,
        is_active=True
    )
    
    # Store in mock database
    mock_users[email] = user
    return user

def clear_mock_users() -> None:
    """Clear all mock users (for development/testing)"""
    mock_users.clear()