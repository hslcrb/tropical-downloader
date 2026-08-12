"""
Tropical Downloader - FastAPI Backend v2.0
Main application entry point
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from backend.routes.api_router import router
from backend.services.download_service import download_service
from backend.services.channel_backup_service import channel_backup_service
from backend.services.websocket_service import ws_service

# Wire WebSocket service into download and channel backup services
download_service.set_ws_service(ws_service)
channel_backup_service.set_ws_service(ws_service)

# Initialize FastAPI application
app = FastAPI(
    title="Tropical Downloader API",
    version="2.0.0",
    description=(
        "Tropical Downloader Backend — "
        "A freedom-preserving YouTube media archive service for democratic citizens. 🌴"
    )
)

# CORS: allow Electron renderer (file://) and localhost Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Global Exception Handlers ───────────────────────────────────────────────
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"success": False, "error": "Validation error", "details": exc.errors()}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": str(exc)}
    )


# ─── Health Check ────────────────────────────────────────────────────────────
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Tropical Downloader API v2.0",
        "status": "running",
        "mission": "정보의 자유 보전 — Preserving freedom of information 🌴"
    }


# ─── Include Router ──────────────────────────────────────────────────────────
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=8765,
        log_level="info",
        reload=False
    )
