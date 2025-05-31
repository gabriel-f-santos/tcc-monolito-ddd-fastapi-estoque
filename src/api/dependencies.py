# src/api/dependencies.py
"""FastAPI dependencies."""

from typing import AsyncGenerator, Optional

import structlog
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import get_settings
from src.shared.infrastructure.database.connection import get_async_session
from src.identity.infrastructure.repositories.sqlalchemy_usuario_repository import (
    SqlAlchemyUsuarioRepository
)
from src.identity.domain.entities.usuario import Usuario

logger = structlog.get_logger()
settings = get_settings()
security = HTTPBearer()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Database dependency."""
    async for session in get_async_session():
        yield session


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> Usuario:
    """Get current authenticated user."""
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode JWT token
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
    except JWTError as e:
        logger.warning("JWT decode error", error=str(e))
        raise credentials_exception
    
    # Get user from database
    user_repo = SqlAlchemyUsuarioRepository(db)
    user = await user_repo.get_by_id(user_id)
    
    if user is None:
        logger.warning("User not found", user_id=user_id)
        raise credentials_exception
    
    if not user.ativo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user"
        )
    
    return user


async def get_current_active_user(
    current_user: Usuario = Depends(get_current_user),
) -> Usuario:
    """Get current active user."""
    if not current_user.ativo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


def require_permission(permission: str):
    """Dependency factory for permission checking."""
    
    async def check_permission(
        current_user: Usuario = Depends(get_current_active_user)
    ) -> Usuario:
        """Check if user has required permission."""
        
        # Check if user has the required permission
        user_permissions = [p.to_string() for p in current_user.permissoes]
        
        if permission not in user_permissions and "admin:*" not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission required: {permission}"
            )
        
        return current_user
    
    return check_permission