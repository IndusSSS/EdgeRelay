"""
EdgeRelay Database Manager
MESSS Compliant - Modular, Efficient, Scalable, Secure, Stable
"""

import logging
from typing import Optional, AsyncGenerator
import asyncpg
import aioredis
from contextlib import asynccontextmanager

from .config import get_settings, get_admin_db_url, get_client_db_url, get_redis_url

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Database manager for handling multiple database connections.
    MESSS Compliant: Modular, Efficient, Secure database management.
    """
    
    def __init__(self, settings):
        self.settings = settings
        self.admin_pool: Optional[asyncpg.Pool] = None
        self.client_pool: Optional[asyncpg.Pool] = None
        self.redis: Optional[aioredis.Redis] = None
        
    async def initialize(self):
        """Initialize database connections."""
        try:
            # Initialize admin database pool
            await self._init_admin_db()
            
            # Initialize client database pool
            await self._init_client_db()
            
            # Initialize Redis connection
            await self._init_redis()
            
            logger.info("✅ All database connections initialized")
            
        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")
            raise
    
    async def _init_admin_db(self):
        """Initialize admin database connection pool."""
        try:
            admin_url = get_admin_db_url()
            self.admin_pool = await asyncpg.create_pool(
                admin_url,
                min_size=2,
                max_size=10,
                command_timeout=30
            )
            logger.info("✅ Admin database pool initialized")
            
        except Exception as e:
            logger.error(f"❌ Admin database initialization failed: {e}")
            raise
    
    async def _init_client_db(self):
        """Initialize client database connection pool."""
        try:
            client_url = get_client_db_url()
            self.client_pool = await asyncpg.create_pool(
                client_url,
                min_size=2,
                max_size=10,
                command_timeout=30
            )
            logger.info("✅ Client database pool initialized")
            
        except Exception as e:
            logger.error(f"❌ Client database initialization failed: {e}")
            raise
    
    async def _init_redis(self):
        """Initialize Redis connection."""
        try:
            redis_url = get_redis_url()
            self.redis = await aioredis.from_url(redis_url, decode_responses=True)
            await self.redis.ping()
            logger.info("✅ Redis connection initialized")
            
        except Exception as e:
            logger.error(f"❌ Redis initialization failed: {e}")
            raise
    
    @asynccontextmanager
    async def get_admin_connection(self) -> AsyncGenerator[asyncpg.Connection, None]:
        """Get admin database connection."""
        if not self.admin_pool:
            raise RuntimeError("Admin database pool not initialized")
        
        async with self.admin_pool.acquire() as connection:
            yield connection
    
    @asynccontextmanager
    async def get_client_connection(self) -> AsyncGenerator[asyncpg.Connection, None]:
        """Get client database connection."""
        if not self.client_pool:
            raise RuntimeError("Client database pool not initialized")
        
        async with self.client_pool.acquire() as connection:
            yield connection
    
    async def get_redis(self) -> aioredis.Redis:
        """Get Redis connection."""
        if not self.redis:
            raise RuntimeError("Redis connection not initialized")
        return self.redis
    
    async def check_admin_db_health(self) -> bool:
        """Check admin database health."""
        try:
            async with self.get_admin_connection() as conn:
                await conn.fetchval("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"Admin database health check failed: {e}")
            return False
    
    async def check_client_db_health(self) -> bool:
        """Check client database health."""
        try:
            async with self.get_client_connection() as conn:
                await conn.fetchval("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"Client database health check failed: {e}")
            return False
    
    async def check_redis_health(self) -> bool:
        """Check Redis health."""
        try:
            redis = await self.get_redis()
            await redis.ping()
            return True
        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            return False
    
    async def close(self):
        """Close all database connections."""
        try:
            if self.admin_pool:
                await self.admin_pool.close()
                logger.info("✅ Admin database pool closed")
            
            if self.client_pool:
                await self.client_pool.close()
                logger.info("✅ Client database pool closed")
            
            if self.redis:
                await self.redis.close()
                logger.info("✅ Redis connection closed")
                
        except Exception as e:
            logger.error(f"❌ Error closing database connections: {e}")
