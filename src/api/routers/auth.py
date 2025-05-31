# src/api/routers/auth.py
"""Authentication API routes."""

from typing import Annotated

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import get_db, get_current_active_user
from src.identity.application.services.auth_application_service import AuthApplicationService
from src.identity.application.dto.auth_dto import LoginDTO, TokenResponseDTO, ChangePasswordDTO
from src.identity.domain.entities.usuario import Usuario
from src.shared.domain.exceptions.base import ValidationException, BusinessRuleException

logger = structlog.get_logger()
router = APIRouter()


@router.post("/login", response_model=TokenResponseDTO)
async def login(
    login_dto: LoginDTO,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """User login endpoint."""
    try:
        auth_service = AuthApplicationService(db)
        token_response = await auth_service.login(login_dto)
        
        return token_response
        
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message
        )
    except BusinessRuleException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.message
        )
    except Exception as e:
        logger.error("Login endpoint error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/change-password")
async def change_password(
    change_password_dto: ChangePasswordDTO,
    current_user: Annotated[Usuario, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Change user password."""
    try:
        auth_service = AuthApplicationService(db)
        success = await auth_service.change_password(
            str(current_user.id), 
            change_password_dto
        )
        
        return {"message": "Password changed successfully"}
        
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )
    except Exception as e:
        logger.error("Change password endpoint error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/me", response_model=dict)
async def get_current_user_info(
    current_user: Annotated[Usuario, Depends(get_current_active_user)]
):
    """Get current user information."""
    return {
        "id": str(current_user.id),
        "email": current_user.email.valor,
        "nome": current_user.nome,
        "permissoes": [p.to_string() for p in current_user.permissoes],
        "ativo": current_user.ativo
    }
