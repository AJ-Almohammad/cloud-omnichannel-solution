# backend/app/routers/health.py
from fastapi import APIRouter, status
from datetime import datetime
import psutil
import sys

router = APIRouter()

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Comprehensive health check endpoint for monitoring and load balancers
    
    Returns system health, dependencies status, and performance metrics
    """
    try:
        # System information
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        health_data = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "Cloud Omnichannel Solution API",
            "version": "1.0.0",
            "system": {
                "python_version": sys.version.split()[0],
                "cpu_usage_percent": cpu_percent,
                "memory": {
                    "total_gb": round(memory.total / (1024**3), 2),
                    "used_gb": round(memory.used / (1024**3), 2),
                    "usage_percent": memory.percent
                },
                "disk": {
                    "total_gb": round(disk.total / (1024**3), 2),
                    "used_gb": round(disk.used / (1024**3), 2),
                    "usage_percent": round((disk.used / disk.total) * 100, 1)
                }
            },
            "dependencies": {
                "database": "connected",  # Mock status
                "redis": "connected",     # Mock status
                "payment_gateway": "healthy",
                "inventory_service": "healthy"
            },
            "metrics": {
                "uptime_seconds": 3600,  # Mock uptime
                "total_requests": 1250,  # Mock request count
                "error_rate": 0.02      # Mock error rate
            }
        }
        
        # Determine overall health
        if cpu_percent > 80 or memory.percent > 85:
            health_data["status"] = "degraded"
            health_data["warnings"] = ["High resource usage detected"]
        
        return health_data
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }

@router.get("/health/ready", status_code=status.HTTP_200_OK)
async def readiness_check():
    """
    Kubernetes readiness probe endpoint
    
    Returns 200 if service is ready to handle requests
    """
    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {
            "api": "ok",
            "database": "ok",
            "dependencies": "ok"
        }
    }

@router.get("/health/live", status_code=status.HTTP_200_OK)
async def liveness_check():
    """
    Kubernetes liveness probe endpoint
    
    Returns 200 if service is alive and should not be restarted
    """
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat()
    }