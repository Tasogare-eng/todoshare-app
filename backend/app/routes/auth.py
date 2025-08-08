from fastapi import APIRouter, HTTPException, Depends, status
from app.models.user import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_service import auth_service
from app.core.dependencies import get_current_active_user
from app.core.security import validate_password_strength
from app.core.mock_auth import clear_mock_users
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate):
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
        user = await auth_service.create_user(user_data)
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
async def login(user_data: UserLogin):
    """Login user"""
    try:
        # Authenticate user
        user = await auth_service.authenticate_user(
            user_data.email, 
            user_data.password
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

@router.post("/debug/clear-users")
async def clear_all_mock_users():
    """Clear all mock users (development only)"""
    clear_mock_users()
    return {"message": "All mock users cleared"}