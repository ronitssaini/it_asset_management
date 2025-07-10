from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.dependencies import get_db
from backend.auth.dependencies import admin_required, manager_or_admin_required
from backend.models.asset import Asset
from pydantic import BaseModel
from typing import List, Optional

# This is the critical line - must create the router instance
router = APIRouter(prefix="/assets", tags=["assets"])

# Pydantic schema for asset input/output
class AssetIn(BaseModel):
    company_name: str
    device_type: str
    serial_number: str
    location: str
    make: Optional[str] = None
    os_version: Optional[str] = None
    ip_address: Optional[str] = None
    subnet_mask: Optional[str] = None
    purchase_date: Optional[str] = None
    additional_device: Optional[str] = None
    remarks: Optional[str] = None
    employee_code: Optional[str] = None
    employee_name: Optional[str] = None
    function: Optional[str] = None
    role: Optional[str] = None
    class Config:
        from_attributes = True

class AssetOut(AssetIn):
    class Config:
        from_attributes = True

def asset_to_dict(asset):
    return {c.name: getattr(asset, c.name) for c in asset.__table__.columns}

@router.get("/", response_model=List[AssetOut])
def get_assets(db: Session = Depends(get_db), role: str = Depends(manager_or_admin_required)):
    assets = db.query(Asset).all()
    return assets

@router.post("/", response_model=AssetOut, status_code=status.HTTP_201_CREATED)
def create_asset(asset: AssetIn, db: Session = Depends(get_db)):
    # Check for duplicate serial number
    if db.query(Asset).filter_by(serial_number=asset.serial_number).first():
        raise HTTPException(status_code=400, detail="Asset with this serial number already exists.")
    data = asset.dict()
    for k, v in data.items():
        if isinstance(v, str) and v.strip() == "":
            data[k] = None
    db_asset = Asset(**data)
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router.delete("/{serial_number}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset(serial_number: str, db: Session = Depends(get_db), role: str = Depends(admin_required)):
    asset = db.query(Asset).filter_by(serial_number=serial_number).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found.")
    db.delete(asset)
    db.commit()
    return