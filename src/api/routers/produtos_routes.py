# src/inventory/presentation/api/v1/produto_routes.py
"""Product API routes."""

from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import get_db, require_permission
from src.produto.application.services.produto_application_service import ProdutoApplicationService
from src.produto.application.dto.produto_dto import (
    ProdutoCreateDTO,
    ProdutoUpdateDTO,
    ProdutoResponseDTO,
    ProdutoListResponseDTO,
    ProdutoSearchDTO
)
#Depends
from fastapi import Depends
from src.identidade.domain.entities.usuario import Usuario
from src.shared.domain.exceptions.base import ValidationException, BusinessRuleException

router = APIRouter(prefix="/api/v1/products")


@router.post("/", response_model=ProdutoResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_product(
    create_dto: ProdutoCreateDTO,
    _: Annotated[Usuario, Depends(require_permission("estoque:write"))],
    db: AsyncSession = Depends(get_db),
):
    """Create new product."""
    service = ProdutoApplicationService(db)
    return await service.create_product(create_dto)


@router.get("/{product_id}", response_model=ProdutoResponseDTO)
async def get_product(
    _: Annotated[Usuario, Depends(require_permission("estoque:write"))],
    product_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get product by ID."""
    service = ProdutoApplicationService(db)
    product = await service.get_product_by_id(product_id)
    
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product not found: {product_id}"
        )
    
    return product


@router.get("/sku/{sku}", response_model=ProdutoResponseDTO)
async def get_product_by_sku(
    _: Annotated[Usuario, Depends(require_permission("estoque:write"))],
    sku: str,
    db: AsyncSession = Depends(get_db)
):
    """Get product by SKU."""
    service = ProdutoApplicationService(db)
    product = await service.get_product_by_sku(sku)
    
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product not found with SKU: {sku}"
        )
    
    return product


@router.get("/", response_model=ProdutoListResponseDTO)
async def list_products(
    _: Annotated[Usuario, Depends(require_permission("estoque:write"))],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """List products with pagination."""
    service = ProdutoApplicationService(db)
    return await service.get_products(skip, limit)


@router.post("/search", response_model=ProdutoListResponseDTO)
async def search_products(
    _: Annotated[Usuario, Depends(require_permission("estoque:write"))],
    search_dto: ProdutoSearchDTO,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """Search products."""
    service = ProdutoApplicationService(db)
    return await service.search_products(search_dto, skip, limit)


@router.put("/{product_id}", response_model=ProdutoResponseDTO)
async def update_product(
    _: Annotated[Usuario, Depends(require_permission("estoque:write"))],
    product_id: UUID,
    update_dto: ProdutoUpdateDTO,
    db: AsyncSession = Depends(get_db)
):
    """Update product."""
    service = ProdutoApplicationService(db)
    product = await service.update_product(product_id, update_dto)
    
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product not found: {product_id}"
        )
    
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    _: Annotated[Usuario, Depends(require_permission("estoque:write"))],
    product_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Delete product."""
    service = ProdutoApplicationService(db)
    success = await service.delete_product(product_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product not found: {product_id}"
        )


@router.get("/category/{categoria}", response_model=ProdutoListResponseDTO)
async def get_products_by_category(
    _: Annotated[Usuario, Depends(require_permission("estoque:write"))],
    categoria: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """Get products by category."""
    service = ProdutoApplicationService(db)
    return await service.get_products_by_category(categoria, skip, limit)