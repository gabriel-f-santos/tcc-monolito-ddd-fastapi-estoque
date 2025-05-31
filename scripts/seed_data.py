# scripts/seed_data.py
#!/usr/bin/env python3
"""Seed initial data script."""

import asyncio
import sys
from pathlib import Path

import structlog

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.config import get_settings
from src.shared.infrastructure.database.connection import init_db, get_async_session
from src.shared.infrastructure.logging.setup import setup_logging
from src.identidade.application.services.usuario_application_service import UsuarioApplicationService
from src.identidade.application.dto.usuario_dto import UsuarioCreateDTO

logger = structlog.get_logger()
settings = get_settings()


async def create_admin_user():
    """Create initial admin user."""
    try:
        async for session in get_async_session():
            user_service = UsuarioApplicationService(session)
            
            # Check if admin user already exists
            try:
                admin_dto = UsuarioCreateDTO(
                    email="admin@inventory.com",
                    nome="System Administrator",
                    senha="admin123",
                    permissoes=["admin:*"],
                    ativo=True
                )
                
                user = await user_service.create_user(admin_dto)
                logger.info("Admin user created", user_id=str(user.id))
                
            except Exception as e:
                if "already exists" in str(e):
                    logger.info("Admin user already exists")
                else:
                    raise
            
            break
        
    except Exception as e:
        logger.error("Failed to create admin user", error=str(e))
        raise


async def main():
    """Main seed function."""
    setup_logging("INFO", "text")
    logger.info("Starting data seeding")
    
    # Initialize database
    await init_db(settings.database_url)
    
    # Create admin user
    await create_admin_user()
    
    logger.info("Data seeding completed successfully")


if __name__ == "__main__":
    asyncio.run(main())
