"""
EdgeRelay Client API Router
MESSS Compliant - Modular, Efficient, Scalable, Secure, Stable
"""

import logging
import uuid
from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from ..core.database import DatabaseManager
from ..core.security import SecurityManager

logger = logging.getLogger(__name__)
router = APIRouter()
security = HTTPBearer()


# Pydantic models
class ClientLoginRequest(BaseModel):
    username: str
    password: str


class ClientResponse(BaseModel):
    client_id: str
    username: str
    full_name: str
    company_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class ClientLoginResponse(BaseModel):
    access_token: str
    token_type: str
    client: ClientResponse


async def get_current_client(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    request: Request = None
) -> Dict[str, Any]:
    """
    Get current authenticated client.
    MESSS Compliant: Secure authentication.
    """
    try:
        security_manager = request.app.state.security_manager
        
        # Verify token
        payload = security_manager.verify_token(credentials.credentials)
        
        # Check if user is client
        if payload.get("role") != "client":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Client access required"
            )
        
        return payload
        
    except Exception as e:
        logger.error(f"Client authentication failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )


@router.post("/auth/login", response_model=ClientLoginResponse)
async def client_login(
    request: ClientLoginRequest,
    req: Request = None
):
    """
    Client login endpoint.
    MESSS Compliant: Secure authentication.
    """
    try:
        db_manager = req.app.state.db_manager
        security_manager = req.app.state.security_manager
        
        # Get client database connection
        async with db_manager.get_client_connection() as conn:
            # Find client by username
            client = await conn.fetchrow(
                """
                SELECT client_id, username, password_hash, full_name, company_name, is_active, created_at, updated_at
                FROM client_users 
                WHERE username = $1 AND is_active = true
                """,
                request.username
            )
            
            if not client:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )
            
            # Verify password
            if not security_manager.verify_password(request.password, client['password_hash']):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )
            
            # Create access token
            access_token = security_manager.create_access_token({
                "client_id": str(client['client_id']),
                "username": client['username'],
                "role": "client",
                "company_name": client['company_name'],
                "sub": str(client['client_id'])
            })
            
            logger.info(f"Client logged in: {client['username']} from {client['company_name']}")
            
            return ClientLoginResponse(
                access_token=access_token,
                token_type="bearer",
                client=ClientResponse(
                    client_id=str(client['client_id']),
                    username=client['username'],
                    full_name=client['full_name'],
                    company_name=client['company_name'],
                    is_active=client['is_active'],
                    created_at=client['created_at'],
                    updated_at=client['updated_at']
                )
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Client login failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.get("/auth/me", response_model=ClientResponse)
async def get_current_client_info(
    current_client: Dict[str, Any] = Depends(get_current_client),
    req: Request = None
):
    """
    Get current client information.
    MESSS Compliant: Efficient user information retrieval.
    """
    try:
        db_manager = req.app.state.db_manager
        client_id = current_client.get("client_id")
        
        async with db_manager.get_client_connection() as conn:
            client = await conn.fetchrow(
                """
                SELECT client_id, username, full_name, company_name, is_active, created_at, updated_at
                FROM client_users 
                WHERE client_id = $1
                """,
                uuid.UUID(client_id)
            )
            
            if not client:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Client not found"
                )
            
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
        logger.error(f"Get client info failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get client information"
        )


@router.post("/auth/logout")
async def client_logout(
    current_client: Dict[str, Any] = Depends(get_current_client)
):
    """
    Client logout endpoint.
    MESSS Compliant: Secure logout.
    """
    try:
        # In a stateless JWT system, logout is handled client-side
        logger.info(f"Client logged out: {current_client.get('username')} from {current_client.get('company_name')}")
        
        return {
            "message": "Successfully logged out",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Client logout failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )


@router.get("/status")
async def get_client_status(
    current_client: Dict[str, Any] = Depends(get_current_client)
):
    """
    Get client status information.
    MESSS Compliant: Efficient status retrieval.
    """
    try:
        return {
            "client_id": current_client.get("client_id"),
            "username": current_client.get("username"),
            "company_name": current_client.get("company_name"),
            "status": "active",
            "timestamp": datetime.utcnow().isoformat(),
            "permissions": {
                "view_cameras": True,
                "receive_alerts": True,
                "control_ptz": True,
                "view_recordings": True
            }
        }
        
    except Exception as e:
        logger.error(f"Get client status failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get client status"
        )
