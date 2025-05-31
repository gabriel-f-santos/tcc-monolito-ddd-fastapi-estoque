# src/api/routers/estoque.py
"""Inventory management API routes."""

from fastapi import APIRouter

router = APIRouter()

# TODO: Implement inventory routes
@router.get("/")
async def get_estoque():
    """Get inventory."""
    return {"message": "Inventory endpoint - TODO"}
