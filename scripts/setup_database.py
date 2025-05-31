# scripts/setup_database.py
#!/usr/bin/env python3
"""Database setup script."""

import asyncio
import sys
from pathlib import Path

import asyncpg
import structlog
from sqlalchemy import text

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.config import get_settings
from src.shared.infrastructure.database.connection import init_db, get_sync_session
from src.shared.infrastructure.logging.setup import setup_logging

logger = structlog.get_logger()
settings = get_settings()


async def create_schemas():
    """Create database schemas."""
    try:
        await init_db(settings.database_url)
        
        # Use sync session for schema creation
        with get_sync_session() as session:
            # Create schemas
            schemas = ["identity", "inventory", "reporting"]
            
            for schema in schemas:
                try:
                    session.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
                    logger.info(f"Schema {schema} created/verified")
                except Exception as e:
                    logger.error(f"Failed to create schema {schema}", error=str(e))
                    raise
            
            session.commit()
            logger.info("All schemas created successfully")
        
        return True
        
    except Exception as e:
        logger.error("Failed to create schemas", error=str(e))
        return False


async def main():
    """Main setup function."""
    setup_logging("INFO", "text")
    logger.info("Starting database setup")
    
    # Create schemas
    if not await create_schemas():
        logger.error("Failed to create schemas")
        sys.exit(1)
    
    logger.info("Database setup completed successfully")
    logger.info("Run 'alembic upgrade head' to apply migrations")


if __name__ == "__main__":
    asyncio.run(main())