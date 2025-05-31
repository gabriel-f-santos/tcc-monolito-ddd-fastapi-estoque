# src/api/routers/relatorios.py
"""Reports API routes."""

from fastapi import APIRouter

router = APIRouter()

# TODO: Implement reports routes
@router.get("/")
async def get_relatorios():
    """Get reports."""
    return {"message": "Reports endpoint - TODO"}