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


async def create_database_if_not_exists():
    """Create database if it doesn't exist."""
    # Parse database URL
    db_url = settings.database_url
    if "://" in db_url:
        # postgresql://user:password@host:port/database
        parts = db_url.split("://")[1]
        auth_host, db_name = parts.rsplit("/", 1)
        if "@" in auth_host:
            auth, host_port = auth_host.split("@")
            username, password = auth.split(":")
        else:
            host_port = auth_host
            username = password = None
        
        if ":" in host_port:
            host, port = host_port.split(":")
            port = int(port)
        else:
            host = host_port
            port = 5432
    else:
        logger.error("Invalid database URL format")
        return False
    
    try:
        # Connect to postgres database to create our database
        conn = await asyncpg.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database="postgres"
        )
        
        # Check if database exists
        exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1", db_name
        )
        
        if not exists:
            logger.info(f"Creating database: {db_name}")
            await conn.execute(f'CREATE DATABASE "{db_name}"')
            logger.info(f"Database {db_name} created successfully")
        else:
            logger.info(f"Database {db_name} already exists")
        
        await conn.close()
        return True
        
    except Exception as e:
        logger.error("Failed to create database", error=str(e))
        return False


async def create_schemas():
    """Create database schemas."""
    try:
        await init_db(settings.database_url)
        
        # Use sync session for schema creation
        with get_sync_session() as session:
            # Create schemas
            schemas = ["identity", "inventory", "warehouse", "reporting"]
            
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
    
    # Create database
    if not await create_database_if_not_exists():
        logger.error("Failed to create database")
        sys.exit(1)
    
    # Create schemas
    if not await create_schemas():
        logger.error("Failed to create schemas")
        sys.exit(1)
    
    logger.info("Database setup completed successfully")
    logger.info("Run 'alembic upgrade head' to apply migrations")


if __name__ == "__main__":
    asyncio.run(main())