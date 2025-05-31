# src/api/routers/movimentacoes.py
"""Movement management API routes."""

from fastapi import APIRouter

router = APIRouter()

# TODO: Implement movement routes
@router.get("/")
async def get_movimentacoes():
    """Get movements."""
    return {"message": "Movements endpoint - TODO"}