# backend/app/main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time
from typing import Dict, Any
import uvicorn

from app.routers import orders, health
from app.config import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log")
    ]
)

logger = logging.getLogger(__name__)

# Application lifespan manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown events"""
    logger.info("🚀 Cloud Omnichannel Solution starting up...")
    # Startup logic
    app.state.startup_time = time.time()
    logger.info("✅ Application startup complete")
    
    yield  # Application runs here
    
    # Shutdown logic
    logger.info("🛑 Application shutting down...")
    logger.info("✅ Cleanup complete")

# Create FastAPI application
def create_application() -> FastAPI:
    settings = get_settings()
    
    app = FastAPI(
        title="Cloud Omnichannel Solution API",
        description="""
        ## Professional E-commerce Order Management System
        
        This API provides comprehensive order management across multiple sales channels:
        
        ### Features
        * **Multi-channel Orders**: Online, In-store, Mobile app orders
        * **Real-time Analytics**: Order statistics and insights  
        * **Customer Management**: Integrated customer profiles
        * **Inventory Sync**: Real-time inventory updates
        * **Payment Processing**: Secure payment handling
        
        ### Architecture
        * **Cloud-native**: Built for AWS Lambda deployment
        * **Microservices**: Modular, scalable design
        * **RESTful**: Standards-compliant API design
        * **Security**: JWT authentication, rate limiting
        """,
        version="1.0.0",
        contact={
            "name": "Solution Architecture Team",
            "email": "arch@company.com",
        },
        license_info={
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT",
        },
        lifespan=lifespan,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json"
    )
    
    # Security middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.allowed_hosts
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["X-Total-Count", "X-Page-Count"]
    )
    
    # Custom middleware for request logging
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        
        # Log request
        logger.info(f"📥 {request.method} {request.url}")
        
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Add custom headers
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-API-Version"] = "1.0.0"
        
        # Log response
        logger.info(
            f"📤 {request.method} {request.url} - "
            f"Status: {response.status_code} - "
            f"Time: {process_time:.3f}s"
        )
        
        return response
    
    # Include routers
    app.include_router(health.router, tags=["Health"])
    app.include_router(
        orders.router, 
        prefix="/api/v1/orders", 
        tags=["Orders"]
    )
    
    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"❌ Global exception: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "message": "An unexpected error occurred",
                "request_id": getattr(request.state, 'request_id', None)
            }
        )
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail,
                "status_code": exc.status_code,
                "path": str(request.url)
            }
        )
    
    return app

# Create app instance
app = create_application()

# Root endpoint
@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint with API information"""
    return {
        "message": "🚀 Cloud Omnichannel Solution API",
        "version": "1.0.0",
        "status": "operational",
        "documentation": "/api/docs",
        "health_check": "/health"
    }

# Application info endpoint
@app.get("/info", tags=["System"])
async def get_app_info():
    """Get application information and stats"""
    settings = get_settings()
    uptime = time.time() - app.state.startup_time if hasattr(app.state, 'startup_time') else 0
    
    return {
        "application": {
            "name": "Cloud Omnichannel Solution",
            "version": "1.0.0",
            "environment": settings.environment,
            "uptime_seconds": round(uptime, 2)
        },
        "system": {
            "python_version": "3.9+",
            "framework": "FastAPI",
            "database": "In-Memory (Demo)",
            "cloud_ready": True
        },
        "features": {
            "multi_channel_orders": True,
            "real_time_analytics": True,
            "customer_management": True,
            "inventory_sync": True,
            "payment_processing": True
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