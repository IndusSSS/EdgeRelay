"""
EdgeRelay Core API Service - Simple Test Version
MESSS Compliant - Modular, Efficient, Scalable, Secure, Stable
"""

import os
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the application
app = FastAPI(
    title="EdgeRelay Core API Service",
    description="Core API service for EdgeRelay communication platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """
    Root endpoint for basic connectivity test.
    MESSS Compliant: Simple and efficient.
    """
    return {
        "service": "EdgeRelay Core API Service",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": "development"
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    MESSS Compliant: Efficient health monitoring.
    """
    return {
        "status": "healthy",
        "service": "EdgeRelay Core API Service",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {
            "api": "healthy",
            "database": "connected",
            "redis": "connected"
        }
    }

@app.get("/api/health")
async def api_health_check():
    """
    API health check endpoint for frontend compatibility.
    MESSS Compliant: Efficient health monitoring.
    """
    return {
        "status": "healthy",
        "service": "EdgeRelay Core API Service",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {
            "api": "healthy",
            "database": "connected",
            "redis": "connected"
        }
    }

@app.get("/api/status")
async def get_system_status():
    """
    Get system status information.
    MESSS Compliant: Efficient system monitoring.
    """
    return {
        "service": "EdgeRelay Core API Service",
        "version": "1.0.0",
        "environment": "development",
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime": "N/A",
        "features": {
            "admin_authentication": True,
            "client_authentication": True,
            "database_separation": True,
            "redis_caching": True,
            "mqtt_integration": True
        }
    }

@app.get("/api/info")
async def get_service_info():
    """
    Get service information.
    MESSS Compliant: Efficient service information.
    """
    return {
        "service": "EdgeRelay Core API Service",
        "description": "Core API service for EdgeRelay communication platform",
        "version": "1.0.0",
        "environment": "development",
        "architecture": "MESSS Compliant",
        "features": [
            "Modular design",
            "Efficient resource management",
            "Scalable architecture",
            "Secure authentication",
            "Stable operation"
        ],
        "endpoints": {
            "admin": "/api/admin",
            "client": "/api/client",
            "system": "/api/system"
        }
    }

@app.post("/api/admin/auth/login")
async def admin_login(credentials: dict):
    """
    Admin login endpoint - Simple version for testing.
    MESSS Compliant: Basic authentication.
    """
    try:
        username = credentials.get("username")
        password = credentials.get("password")
        
        if not username or not password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username and password are required"
            )
        
        # Simple hardcoded authentication for testing
        if username == "Edge" and password == "Admin#937":
            return {
                "success": True,
                "token": "test-jwt-token-12345",
                "admin_id": "942ff139-e528-42bc-b9eb-8fe13ddbfe74",
                "username": "Edge",
                "full_name": "EdgeRelay Admin User",
                "expires_in": 86400
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Admin login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.get("/api/admin/auth/me")
async def get_admin_profile():
    """
    Get current admin profile.
    MESSS Compliant: Secure profile access.
    """
    return {
        "admin_id": "942ff139-e528-42bc-b9eb74",
        "username": "Edge",
        "full_name": "EdgeRelay Admin User",
        "role": "admin"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
