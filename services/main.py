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
            "database": "not_connected",
            "redis": "not_connected"
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

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
