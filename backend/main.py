"""
Tropical Downloader - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI application
app = FastAPI(
    title="Tropical Downloader API",
    version="2.0.0",
    description="REST API for Tropical Downloader - YouTube media download service"
)

# CORS configuration (allow Electron localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:*",
        "file://*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Tropical Downloader API v2.0",
        "status": "running"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8765,
        log_level="info",
        reload=False
    )
