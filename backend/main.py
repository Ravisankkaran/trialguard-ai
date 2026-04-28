"""
TrialGuard AI - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from pathlib import Path

# Import routes
from routes.upload import router as upload_router
from routes.process import router as process_router
from routes.predict import router as predict_router
from routes.results import router as results_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="TrialGuard AI API",
    description="Real-time Clinical Trial Monitoring Platform",
    version="0.1.0"
)

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload_router, prefix="/api", tags=["Data Upload"])
app.include_router(process_router, prefix="/api", tags=["Data Processing"])
app.include_router(predict_router, prefix="/api", tags=["Predictions"])
app.include_router(results_router, prefix="/api", tags=["Results"])


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "service": "TrialGuard AI",
        "version": "0.1.0",
        "description": "Real-time Clinical Trial Monitoring Platform",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "TrialGuard AI API"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
