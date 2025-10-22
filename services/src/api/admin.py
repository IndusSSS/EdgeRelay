"""
EdgeRelay Admin API Router
MESSS Compliant - Modular, Efficient, Scalable, Secure, Stable
"""

import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Header, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from ..core.database import DatabaseManager
from ..core.security import SecurityManager
from ..core.config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter()
security = HTTPBearer()


# Pydantic models
class AdminLoginRequest(BaseModel):
    username: str
    password: str


class AdminResponse(BaseModel):
    admin_id: str
    username: str
    full_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class AdminLoginResponse(BaseModel):
    access_token: str
    token_type: str
    admin: AdminResponse


class ClientCreateRequest(BaseModel):
    username: str
    password: str
    full_name: str
    company_name: str


class ClientResponse(BaseModel):
    client_id: str
    username: str
    full_name: str
    company_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


async def get_db_manager(request: Request) -> DatabaseManager:
    """Get database manager from app state."""
    return request.app.state.db_manager


async def get_security_manager(request: Request) -> SecurityManager:
    """Get security manager from app state."""
    return request.app.state.security_manager


async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    request: Request = None
) -> Dict[str, Any]:
    """
    Get current authenticated admin.
    MESSS Compliant: Secure authentication.
    """
    try:
        security_manager = request.app.state.security_manager
        
        # Verify token
        payload = security_manager.verify_token(credentials.credentials)
        
        # Check if user is admin
        if payload.get("role") != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        
        return payload
        
    except Exception as e:
        logger.error(f"Admin authentication failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )


@router.post("/auth/login", response_model=AdminLoginResponse)
async def admin_login(
    request: AdminLoginRequest,
    req: Request = None
):
    """
    Admin login endpoint.
    MESSS Compliant: Secure authentication.
    """
    try:
        db_manager = req.app.state.db_manager
        security_manager = req.app.state.security_manager
        
        # Get admin database connection
        async with db_manager.get_admin_connection() as conn:
            # Find admin by username
            admin = await conn.fetchrow(
                """
                SELECT admin_id, username, password_hash, full_name, is_active, created_at, updated_at
                FROM admin_users 
                WHERE username = $1 AND is_active = true
                """,
                request.username
            )
            
            if not admin:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )
            
            # Verify password
            if not security_manager.verify_password(request.password, admin['password_hash']):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )
            
            # Create access token
            access_token = security_manager.create_access_token({
                "admin_id": str(admin['admin_id']),
                "username": admin['username'],
                "role": "admin",
                "sub": str(admin['admin_id'])
            })
            
            logger.info(f"Admin logged in: {admin['username']}")
            
            return AdminLoginResponse(
                access_token=access_token,
                token_type="bearer",
                admin=AdminResponse(
                    admin_id=str(admin['admin_id']),
                    username=admin['username'],
                    full_name=admin['full_name'],
                    is_active=admin['is_active'],
                    created_at=admin['created_at'],
                    updated_at=admin['updated_at']
                )
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Admin login failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.get("/auth/me", response_model=AdminResponse)
async def get_current_admin_info(
    current_admin: Dict[str, Any] = Depends(get_current_admin),
    req: Request = None
):
    """
    Get current admin information.
    MESSS Compliant: Efficient user information retrieval.
    """
    try:
        db_manager = req.app.state.db_manager
        admin_id = current_admin.get("admin_id")
        
        async with db_manager.get_admin_connection() as conn:
            admin = await conn.fetchrow(
                """
                SELECT admin_id, username, full_name, is_active, created_at, updated_at
                FROM admin_users 
                WHERE admin_id = $1
                """,
                uuid.UUID(admin_id)
            )
            
            if not admin:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Admin not found"
                )
            
            return AdminResponse(
                admin_id=str(admin['admin_id']),
                username=admin['username'],
                full_name=admin['full_name'],
                is_active=admin['is_active'],
                created_at=admin['created_at'],
                updated_at=admin['updated_at']
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get admin info failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get admin information"
        )


@router.post("/auth/logout")
async def admin_logout(
    current_admin: Dict[str, Any] = Depends(get_current_admin)
):
    """
    Admin logout endpoint.
    MESSS Compliant: Secure logout.
    """
    try:
        # In a stateless JWT system, logout is handled client-side
        # Server-side logout would require token blacklisting
        logger.info(f"Admin logged out: {current_admin.get('username')}")
        
        return {
            "message": "Successfully logged out",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Admin logout failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )


@router.post("/clients", response_model=ClientResponse)
async def create_client(
    request: ClientCreateRequest,
    current_admin: Dict[str, Any] = Depends(get_current_admin),
    req: Request = None
):
    """
    Create new client user.
    MESSS Compliant: Secure client creation.
    """
    try:
        db_manager = req.app.state.db_manager
        security_manager = req.app.state.security_manager
        
        # Validate password strength
        if not security_manager.validate_password_strength(request.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password does not meet strength requirements"
            )
        
        # Hash password
        password_hash = security_manager.hash_password(request.password)
        
        # Generate client ID
        client_id = uuid.uuid4()
        
        async with db_manager.get_client_connection() as conn:
            # Check if username already exists
            existing_client = await conn.fetchrow(
                "SELECT client_id FROM client_users WHERE username = $1",
                request.username
            )
            
            if existing_client:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already exists"
                )
            
            # Create client
            client = await conn.fetchrow(
                """
                INSERT INTO client_users (client_id, username, password_hash, full_name, company_name, is_active)
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING client_id, username, full_name, company_name, is_active, created_at, updated_at
                """,
                client_id, request.username, password_hash, request.full_name, request.company_name, True
            )
            
            logger.info(f"Client created: {request.username} by admin: {current_admin.get('username')}")
            
            return ClientResponse(
                client_id=str(client['client_id']),
                username=client['username'],
                full_name=client['full_name'],
                company_name=client['company_name'],
                is_active=client['is_active'],
                created_at=client['created_at'],
                updated_at=client['updated_at']
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Client creation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Client creation failed"
        )


@router.get("/clients", response_model=list[ClientResponse])
async def get_clients(
    current_admin: Dict[str, Any] = Depends(get_current_admin),
    req: Request = None
):
    """
    Get all client users.
    MESSS Compliant: Efficient client retrieval.
    """
    try:
        db_manager = req.app.state.db_manager
        
        async with db_manager.get_client_connection() as conn:
            clients = await conn.fetch(
                """
                SELECT client_id, username, full_name, company_name, is_active, created_at, updated_at
                FROM client_users
                ORDER BY created_at DESC
                """
            )
            
            return [
                ClientResponse(
                    client_id=str(client['client_id']),
                    username=client['username'],
                    full_name=client['full_name'],
                    company_name=client['company_name'],
                    is_active=client['is_active'],
                    created_at=client['created_at'],
                    updated_at=client['updated_at']
                )
                for client in clients
            ]
            
    except Exception as e:
        logger.error(f"Get clients failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get clients"
        )
