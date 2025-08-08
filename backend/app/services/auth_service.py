from typing import Optional
from app.models.user import UserCreate, UserInDB, UserResponse
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.database import get_supabase_client
from app.core.mock_auth import create_mock_user, get_mock_user_by_email, get_mock_user_by_id
from datetime import datetime, timedelta
import uuid
import logging

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self):
        self.supabase = get_supabase_client()
    
    async def create_user(self, user_data: UserCreate) -> Optional[UserResponse]:
        """Create a new user"""
        try:
            # Check if user already exists
            existing_user = await self.get_user_by_email(user_data.email)
            if existing_user:
                return None
            
            # For development without Supabase, create mock user
            if not self.supabase:
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
            
            # Create user in Supabase
            hashed_password = get_password_hash(user_data.password)
            response = self.supabase.table('users').insert({
                'id': str(uuid.uuid4()),
                'email': user_data.email,
                'username': user_data.username,
                'hashed_password': hashed_password,
                'created_at': datetime.utcnow().isoformat(),
                'is_active': True
            }).execute()
            
            if response.data:
                user_dict = response.data[0]
                return UserResponse(**user_dict)
            
            return None
            
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return None
    
    async def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        """Get user by email"""
        try:
            # For development without Supabase, use mock storage
            if not self.supabase:
                return get_mock_user_by_email(email)
            
            response = self.supabase.table('users').select("*").eq('email', email).execute()
            
            if response.data:
                user_dict = response.data[0]
                return UserInDB(**user_dict)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting user by email: {e}")
            return None
    
    async def get_user_by_id(self, user_id: str) -> Optional[UserResponse]:
        """Get user by ID"""
        try:
            # For development without Supabase, use mock storage
            if not self.supabase:
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
            
            response = self.supabase.table('users').select("*").eq('id', user_id).execute()
            
            if response.data:
                user_dict = response.data[0]
                return UserResponse(**user_dict)
            
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