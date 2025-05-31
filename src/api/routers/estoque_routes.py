# src/inventory/presentation/api/v1/estoque_routes.py
"""Inventory API routes."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession


from src.api.dependencies import get_db
from src.estoque.application.services.estoque_application_service import EstoqueApplicationService
from src.estoque.application.dto.estoque_dto import (
    EstoqueCreateDTO,
    EstoqueUpdateDTO,
    EstoqueMovimentacaoDTO,
    EstoqueAjusteDTO,
    EstoqueReservaDTO,
    EstoqueResponseDTO,
    EstoqueListResponseDTO,
    EstoqueBaixoDTO,
    EstoqueZeradoDTO
)

router = APIRouter(prefix="/api/v1/inventory", tags=["inventory"])


@router.post("/", response_model=EstoqueResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_inventory(
    create_dto: EstoqueCreateDTO,
    db: AsyncSession = Depends(get_db)
):
    """Create new inventory record."""
    service = EstoqueApplicationService(db)
    return await service.create_inventory(create_dto)


@router.get("/product/{produto_id}", response_model=EstoqueResponseDTO)
async def get_inventory_by_product(
    produto_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get inventory by product ID."""
    service = EstoqueApplicationService(db)
    inventory = await service.get_inventory_by_product_id(produto_id)
    
    if inventory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory not found for product: {produto_id}"
        )
    
    return inventory


@router.get("/", response_model=EstoqueListResponseDTO)
async def list_inventory(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """List all inventory with pagination."""
    service = EstoqueApplicationService(db)
    return await service.get_all_inventory(skip, limit)


@router.post("/add-stock", response_model=EstoqueResponseDTO)
async def add_stock(
    movimento_dto: EstoqueMovimentacaoDTO,
    db: AsyncSession = Depends(get_db)
):
    """Add stock to product."""
    service = EstoqueApplicationService(db)
    return await service.add_stock(movimento_dto)


@router.post("/remove-stock", response_model=EstoqueResponseDTO)
async def remove_stock(
    movimento_dto: EstoqueMovimentacaoDTO,
    db: AsyncSession = Depends(get_db)
):
    """Remove stock from product."""
    service = EstoqueApplicationService(db)
    return await service.remove_stock(movimento_dto)


@router.post("/adjust-stock", response_model=EstoqueResponseDTO)
async def adjust_stock(
    ajuste_dto: EstoqueAjusteDTO,
    db: AsyncSession = Depends(get_db)
):
    """Adjust stock to new quantity."""
    service = EstoqueApplicationService(db)
    return await service.adjust_stock(ajuste_dto)


@router.post("/reserve", response_model=EstoqueResponseDTO)
async def reserve_stock(
    reserva_dto: EstoqueReservaDTO,
    db: AsyncSession = Depends(get_db)
):
    """Reserve stock."""
    service = EstoqueApplicationService(db)
    return await service.reserve_stock(reserva_dto)


@router.post("/release-reservation", response_model=EstoqueResponseDTO)
async def release_reservation(
    reserva_dto: EstoqueReservaDTO,
    db: AsyncSession = Depends(get_db)
):
    """Release reserved stock."""
    service = EstoqueApplicationService(db)
    return await service.release_reservation(reserva_dto)


@router.get("/reports/low-stock", response_model=EstoqueBaixoDTO)
async def get_low_stock_report(
    db: AsyncSession = Depends(get_db)
):
    """Get low stock report."""
    service = EstoqueApplicationService(db)
    return await service.get_low_stock_report()


@router.get("/reports/out-of-stock", response_model=EstoqueZeradoDTO)
async def get_out_of_stock_report(
    db: AsyncSession = Depends(get_db)
):
    """Get out of stock report."""
    service = EstoqueApplicationService(db)
    return await service.get_out_of_stock_report()