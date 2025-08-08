from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import verify_token
from app.services.auth_service import auth_service
from app.models.user import UserResponse
from typing import Optional

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> UserResponse:
    """
    Dependency to get current authenticated user
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Verify token
        user_id = verify_token(credentials.credentials)
        if user_id is None:
            raise credentials_exception
        
        # Get user from database
        user = await auth_service.get_user_by_id(user_id)
        if user is None:
            raise credentials_exception
        
        return user
        
    except Exception:
        raise credentials_exception

async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)
    )
) -> Optional[UserResponse]:
    """
    Dependency to get current user (optional)
    Returns None if no token provided or invalid
    """
    if not credentials:
        return None
    
    try:
        user_id = verify_token(credentials.credentials)
        if user_id is None:
            return None
        
        user = await auth_service.get_user_by_id(user_id)
        return user
        
    except Exception:
        return None

async def get_current_active_user(
    current_user: UserResponse = Depends(get_current_user)
) -> UserResponse:
    """
    Dependency to get current active user
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user