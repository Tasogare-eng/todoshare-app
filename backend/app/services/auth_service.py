from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import UserCreate, UserInDB, UserResponse, UserCreateFromGoogle
from app.models.db_models import User
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.database import get_db
from datetime import datetime, timedelta
import uuid
import logging

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self):
        pass
    
    async def create_user(self, user_data: UserCreate, db: Session) -> Optional[UserResponse]:
        """Create a new user"""
        try:
            # Check if user already exists
            existing_user = db.query(User).filter(User.email == user_data.email).first()
            if existing_user:
                return None
            
            # Create new user
            hashed_password = get_password_hash(user_data.password)
            db_user = User(
                email=user_data.email,
                username=user_data.username,
                hashed_password=hashed_password
            )
            
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            
            return UserResponse(
                id=db_user.id,
                email=db_user.email,
                username=db_user.username,
                created_at=db_user.created_at,
                is_active=db_user.is_active
            )
            
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            db.rollback()
            return None
    
    async def get_user_by_email(self, email: str, db: Session) -> Optional[User]:
        """Get user by email"""
        try:
            return db.query(User).filter(User.email == email).first()
        except Exception as e:
            logger.error(f"Error getting user by email: {e}")
            return None
    
    async def get_user_by_id(self, user_id: str, db: Session) -> Optional[UserResponse]:
        """Get user by ID"""
        try:
            db_user = db.query(User).filter(User.id == user_id).first()
            if db_user:
                return UserResponse(
                    id=db_user.id,
                    email=db_user.email,
                    username=db_user.username,
                    created_at=db_user.created_at,
                    is_active=db_user.is_active
                )
            return None
            
        except Exception as e:
            logger.error(f"Error getting user by ID: {e}")
            return None
    
    async def authenticate_user(self, email: str, password: str, db: Session) -> Optional[User]:
        """Authenticate user with email and password"""
        user = await self.get_user_by_email(email, db)
        if not user:
            return None
        
        if not user.hashed_password or not verify_password(password, user.hashed_password):
            return None
        
        return user
    
    def create_access_token(self, user_id: str) -> str:
        """Create access token for user"""
        return create_access_token(subject=user_id)
    
    async def get_or_create_google_user(self, user_info: dict, db: Session) -> Optional[UserResponse]:
        """Get existing user or create new user from Google OAuth"""
        try:
            # Check if user exists by email
            existing_user = await self.get_user_by_email(user_info['email'], db)
            if existing_user:
                # Update Google ID if not set
                if not existing_user.google_id:
                    existing_user.google_id = user_info['google_id']
                    existing_user.picture = user_info.get('picture', '')
                    db.commit()
                
                return UserResponse(
                    id=existing_user.id,
                    email=existing_user.email,
                    username=existing_user.username,
                    created_at=existing_user.created_at,
                    is_active=existing_user.is_active
                )
            
            # Create new user from Google info
            username = user_info.get('name', user_info['email'].split('@')[0])
            db_user = User(
                email=user_info['email'],
                username=username,
                google_id=user_info['google_id'],
                picture=user_info.get('picture', ''),
                hashed_password=None  # No password for OAuth users
            )
            
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            
            return UserResponse(
                id=db_user.id,
                email=db_user.email,
                username=db_user.username,
                created_at=db_user.created_at,
                is_active=db_user.is_active
            )
            
        except Exception as e:
            logger.error(f"Error getting or creating Google user: {e}")
            db.rollback()
            return None

# Singleton instance
auth_service = AuthService()