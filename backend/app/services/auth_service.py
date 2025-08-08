from typing import Optional
from app.models.user import UserCreate, UserInDB, UserResponse
from app.core.security import get_password_hash, verify_password, create_access_token
# Removed supabase dependency - using mock storage only
from app.core.mock_auth import create_mock_user, get_mock_user_by_email, get_mock_user_by_id
from datetime import datetime, timedelta
import uuid
import logging

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self):
        # Using mock storage only - no external database
        pass
    
    async def create_user(self, user_data: UserCreate) -> Optional[UserResponse]:
        """Create a new user"""
        try:
            # Check if user already exists
            existing_user = await self.get_user_by_email(user_data.email)
            if existing_user:
                return None
            
            # Create mock user
            mock_user = create_mock_user(
                user_data.email, 
                user_data.username, 
                user_data.password
            )
            return UserResponse(
                id=mock_user.id,
                email=mock_user.email,
                username=mock_user.username,
                created_at=mock_user.created_at,
                is_active=mock_user.is_active
            )
            
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return None
    
    async def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        """Get user by email"""
        try:
            # Use mock storage
            return get_mock_user_by_email(email)
            
        except Exception as e:
            logger.error(f"Error getting user by email: {e}")
            return None
    
    async def get_user_by_id(self, user_id: str) -> Optional[UserResponse]:
        """Get user by ID"""
        try:
            # Use mock storage
            mock_user = get_mock_user_by_id(user_id)
            if mock_user:
                return UserResponse(
                    id=mock_user.id,
                    email=mock_user.email,
                    username=mock_user.username,
                    created_at=mock_user.created_at,
                    is_active=mock_user.is_active
                )
            return None
            
        except Exception as e:
            logger.error(f"Error getting user by ID: {e}")
            return None
    
    async def authenticate_user(self, email: str, password: str) -> Optional[UserInDB]:
        """Authenticate user with email and password"""
        user = await self.get_user_by_email(email)
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        return user
    
    def create_access_token(self, user_id: str) -> str:
        """Create access token for user"""
        return create_access_token(subject=user_id)

# Singleton instance
auth_service = AuthService()