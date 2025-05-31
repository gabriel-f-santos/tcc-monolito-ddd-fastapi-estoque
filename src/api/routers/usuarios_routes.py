# src/api/routers/usuarios.py
"""User management API routes."""

from typing import Annotated
from uuid import UUID

import structlog
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import get_db, require_permission
from src.identidade.application.services.usuario_application_service import UsuarioApplicationService
from src.identidade.application.dto.usuario_dto import (
    UsuarioCreateDTO,
    UsuarioUpdateDTO,
    UsuarioResponseDTO,
    UsuarioListResponseDTO
)
from src.identidade.domain.entities.usuario import Usuario
from src.shared.domain.exceptions.base import ValidationException, BusinessRuleException

logger = structlog.get_logger()
router = APIRouter()


@router.post("/", response_model=UsuarioResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_user(
    create_dto: UsuarioCreateDTO,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[Usuario, Depends(require_permission("usuarios:write"))]
):

    """Create new user."""
    try:
        user_service = UsuarioApplicationService(db)
        user_response = await user_service.create_user(create_dto)
        
        return user_response
        
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )
    except BusinessRuleException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message
        )
    except Exception as e:
        logger.error("Create user endpoint error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/", response_model=UsuarioListResponseDTO)
async def get_users(
    db: Annotated[AsyncSession, Depends(get_db)],
    _ : Annotated[Usuario, Depends(require_permission("usuarios:read"))],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    """Get users with pagination."""
    try:
        user_service = UsuarioApplicationService(db)
        users_response = await user_service.get_users(skip, limit)
        
        return users_response
        
    except Exception as e:
        logger.error("Get users endpoint error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/{user_id}", response_model=UsuarioResponseDTO)
async def get_user(
    user_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[Usuario, Depends(require_permission("usuarios:read"))]
):
    """Get user by ID."""
    try:
        user_service = UsuarioApplicationService(db)
        user_response = await user_service.get_user_by_id(user_id)
        
        if user_response is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return user_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Get user endpoint error", user_id=str(user_id), error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.put("/{user_id}", response_model=UsuarioResponseDTO)
async def update_user(
    user_id: UUID,
    update_dto: UsuarioUpdateDTO,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[Usuario, Depends(require_permission("usuarios:write"))]
):
    """Update user."""
    try:
        user_service = UsuarioApplicationService(db)
        user_response = await user_service.update_user(user_id, update_dto)
        
        if user_response is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return user_response
        
    except HTTPException:
        raise
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )
    except BusinessRuleException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message
        )
    except Exception as e:
        logger.error("Update user endpoint error", user_id=str(user_id), error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[Usuario, Depends(require_permission("usuarios:delete"))]
):
    """Delete user."""
    try:
        user_service = UsuarioApplicationService(db)
        success = await user_service.delete_user(user_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Delete user endpoint error", user_id=str(user_id), error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )