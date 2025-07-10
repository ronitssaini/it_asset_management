# Explicitly import and expose the router instances
from .assets import router as assets
from .upload import router as upload
from .auth import router as auth

# Optional: You can also expose other items if needed
__all__ = ["assets", "upload", "auth"]

# Add this to serve the add_asset.html page
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), '../../frontend/templates'))

router_add_asset_page = APIRouter()

@router_add_asset_page.get('/add_asset', response_class=HTMLResponse)
def add_asset_page(request: Request):
    return templates.TemplateResponse('add_asset.html', {"request": request})