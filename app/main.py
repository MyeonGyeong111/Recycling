from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app.include_router(api_router, prefix=settings.API_V1_STR)

frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")

@app.on_event("startup")
async def startup_event():
    if os.path.exists(frontend_path):
        app.mount("/assets", StaticFiles(directory=os.path.join(frontend_path, "assets")), name="assets")

@app.get("/{full_path:path}", include_in_schema=False)
async def serve_frontend(full_path: str):
    if not os.path.exists(frontend_path):
        return {"message": "Frontend is building or not found. Go to /docs for API."}
    
    file_path = os.path.join(frontend_path, full_path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
    return FileResponse(os.path.join(frontend_path, "index.html"))
