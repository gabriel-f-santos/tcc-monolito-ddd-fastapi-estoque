# Placeholder files for other routers
# src/api/routers/produtos.py
"""Product management API routes."""

from fastapi import APIRouter

router = APIRouter()

# TODO: Implement product routes
@router.get("/")
async def get_produtos():
    """Get products."""
    return {"message": "Products endpoint - TODO"}
