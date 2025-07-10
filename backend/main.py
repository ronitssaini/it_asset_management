from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from sqlalchemy.orm import Session
from backend.database.session import engine
from backend.dependencies import get_db
from backend.routers.assets import router as assets_router
from backend.routers.upload import router as upload_router
from backend.routers.auth import router as auth_router
from backend.models.asset import Asset

# Create tables (temporary for development)
from backend.models import asset, user
asset.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="IT Asset Management API",
    description="API for managing IT assets in an organization.",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Templates
templates = Jinja2Templates(directory="frontend/templates")

# Include routers
app.include_router(auth_router)
app.include_router(assets_router)
app.include_router(upload_router)

# CORS middleware (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}

# Frontend routes
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.get("/analytics", response_class=HTMLResponse)
async def analytics_page(request: Request):
    return templates.TemplateResponse("analytics.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/admin/approvals", response_class=HTMLResponse)
async def admin_approvals_page(request: Request):
    return templates.TemplateResponse("admin_approvals.html", {"request": request})

@app.get("/add_asset", response_class=HTMLResponse)
async def add_asset_page(request: Request):
    return templates.TemplateResponse("add_asset.html", {"request": request})

@app.get("/", response_class=HTMLResponse, tags=["Landing"])
def landing_page(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})