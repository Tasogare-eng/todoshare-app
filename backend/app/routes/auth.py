from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.models.user import UserCreate, UserLogin, UserResponse, Token, GoogleLoginRequest
from app.services.auth_service import auth_service
from app.core.dependencies import get_current_active_user
from app.core.database import get_db
from app.core.security import validate_password_strength
from app.services.google_auth import google_auth_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        # Validate password strength
        is_valid, error_message = validate_password_strength(user_data.password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )
        
        # Create user
        user = await auth_service.create_user(user_data, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    try:
        # Authenticate user
        user = await auth_service.authenticate_user(
            user_data.email, 
            user_data.password,
            db
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token = auth_service.create_access_token(user.id)
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=30 * 60  # 30 minutes in seconds
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/logout")
async def logout(current_user: UserResponse = Depends(get_current_active_user)):
    """Logout user"""
    # In a real implementation, you would invalidate the token
    # For now, we just return a success message
    # Client should remove the token from storage
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Get current user info"""
    return current_user

@router.post("/refresh")
async def refresh_token(
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Refresh access token"""
    try:
        # Create new access token
        access_token = auth_service.create_access_token(current_user.id)
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=30 * 60  # 30 minutes in seconds
        )
        
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/google-login", response_model=Token)
async def google_login(google_data: GoogleLoginRequest, db: Session = Depends(get_db)):
    """Login with Google"""
    try:
        # Verify Google ID token
        user_info = google_auth_service.verify_google_token(google_data.id_token)
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Google token"
            )
        
        # Check if user exists or create new user
        user = await auth_service.get_or_create_google_user(user_info, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create or retrieve user"
            )
        
        # Create access token
        access_token = auth_service.create_access_token(user.id)
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=30 * 60  # 30 minutes in seconds
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Google login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/debug/clear-users")
async def clear_all_users(db: Session = Depends(get_db)):
    """Clear all users (development only)"""
    from app.models.db_models import User, Category, Todo
    
    # Delete in correct order due to foreign keys
    db.query(Todo).delete()
    db.query(Category).delete()
    db.query(User).delete()
    db.commit()
    
    return {"message": "All users and related data cleared"}